import base64
import logging

import PIL
import torch
from torch import nn
from transformers import DetrFeatureExtractor, DetrForObjectDetection
from transformers.models.detr.feature_extraction_detr import \
    center_to_corners_format

MODEL_DIR = "/app/build/"


# because of hugging faces detr postprocessing is not working with GPU atm
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


class ObjectDetection(object):

    def __init__(self,
                 feature_extractor_path=MODEL_DIR,
                 model_path=MODEL_DIR
                 ):
        print("Initializing")
        self.torch_device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.feature_extractor = DetrFeatureExtractor.from_pretrained(feature_extractor_path)
        self.model = DetrForObjectDetection.from_pretrained(model_path)
        self.model = self.model.to(self.torch_device)
        self.log = logging.getLogger()
        self.log.info(f"Initialized for device: {self.torch_device}")

    def predict_raw(self, msg):
        self.log.info(f"Predict Raw invoked!")

        size = tuple([int(s) for s in msg['size'].split("x")])
        mode = msg['mode']
        image_bytes = base64.b64decode(msg['media'])

        image = PIL.Image.frombytes(mode, size, image_bytes)

        self.log.debug(f"Image from bytes created")
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        inputs = inputs.to(self.torch_device)
        self.log.debug(f"Features extracted")
        outputs = self.model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        self.log.debug("Convert results")
        target_sizes = torch.tensor([image.size[::-1]])
        results = post_process(outputs, target_sizes=target_sizes,
                               torch_device=self.torch_device)[0]

        output = []
        for score, label, box in zip(results["scores"], results["labels"],
                                     results["boxes"]):
            if score.item() > 0.01:
                box = [round(i, 2) for i in box.tolist()]
                output.append({
                    "label": self.model.config.id2label[label.item()],
                    "score": score.item(),
                    "box": box
                })

        self.log.info(f"Results: {output}")
        return output
