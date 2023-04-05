import base64
import json
import logging
import time

import requests
from PIL import Image

from ObjectDetection import ObjectDetection
logging.basicConfig(level=logging.INFO)

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
cat_image = Image.open(requests.get(url, stream=True).raw)

files = {
    "mode": cat_image.mode,
    "size": "640x480",
    "media": base64.b64encode(cat_image.tobytes())
}

# MODEL_ENDPOINT = "http://localhost:9000/api/v0.1/predictions"
#
# start = time.time()
# results = requests.post(MODEL_ENDPOINT, files=files)
# print(f"Request time: {time.time() - start}")
#
# print(f"Result code {results.status_code}")
# res = json.loads(results.text)
#
# for r in res:
#     if r['score'] > 0.9:
#         print(
#             f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
#         )

# Local model execution
model = ObjectDetection(
    feature_extractor_path="./build/",
    model_path="./build/"
)

start=time.time()
res = model.predict_raw(files)
print(f"Request time: {time.time()-start}")

for r in res:
    if r['score'] > 0.9:
        print(
            f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
        )
