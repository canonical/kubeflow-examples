import requests
import torch
from PIL import Image
from torch import nn
from transformers import DetrFeatureExtractor, DetrForObjectDetection
from transformers.models.detr.feature_extraction_detr import \
    center_to_corners_format

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
img = Image.open(requests.get(url, stream=True).raw)
img.convert("L")


# because of hugging faces postprocessing is not working with GPU
def post_process(outputs, target_sizes, torch_device):
    out_logits, out_bbox = outputs.logits, outputs.pred_boxes

    if len(out_logits) != len(target_sizes):
        raise ValueError(
            "Make sure that you pass in as many target sizes as the batch dimension of the logits")
    if target_sizes.shape[1] != 2:
        raise ValueError(
            "Each element of target_sizes must contain the size (h, w) of each image of the batch")

    prob = nn.functional.softmax(out_logits, -1)
    scores, labels = prob[..., :-1].max(-1)

    # convert to [x0, y0, x1, y1] format
    boxes = center_to_corners_format(out_bbox)
    # and from relative [0, 1] to absolute [0, height] coordinates
    img_h, img_w = target_sizes.unbind(1)
    scale_fct = torch.stack([img_w, img_h, img_w, img_h], dim=1).to(
        torch_device)
    boxes = boxes * scale_fct[:, None, :]

    results = [{"scores": s, "labels": l, "boxes": b} for s, l, b in
               zip(scores, labels, boxes)]
    return results


torch_device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(torch_device)

feature_extractor = DetrFeatureExtractor.from_pretrained(
    "facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50").to(
    torch_device)

import time
start = time.time()
# img = Image.open("../data/frame_screenshot_06.08.2022.png")
inputs = feature_extractor(images=img, return_tensors="pt").to(torch_device)
print(f"Feature extraction: {time.time()-start}s")
outputs = model(**inputs)
print(f"Model inference: {time.time()-start}s")

# convert outputs (bounding boxes and class logits) to COCO API
target_sizes = torch.tensor([img.size[::-1]])

# results = feature_extractor.post_process(outputs, target_sizes=target_sizes)[0]
results = post_process(
    outputs, target_sizes=target_sizes, torch_device=torch_device)[0]
print(f"Postprocessing: {time.time()-start}s")

res = []
for score, label, box in zip(results["scores"], results["labels"],
                             results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    res.append({
        "label": model.config.id2label[label.item()],
        "score": score.item(),
        "box": box
    })

for r in res:
    if r['score'] > 0.9:
        print(
            f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
        )
