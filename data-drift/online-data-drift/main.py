import uuid

from flask import Flask, request
import mlflow
import numpy as np
import json
import requests
import os

app = Flask(__name__)

loaded_model = mlflow.pyfunc.load_model('./model/')
result_broker_url = os.environ['BROKER_URL']


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/', methods=['POST'])
def hello_world():
    input_data = json.loads(request.data)
    app.logger.info(input_data)

    drift_prediction = loaded_model.predict(input_data['data']['ndarray'])
    app.logger.info(drift_prediction)

    response = requests.post(
        url=result_broker_url,
        data=json.dumps(drift_prediction, cls=NumpyEncoder),
        headers={
            "Content-Type": "application/json",
            "Ce-Id": str(uuid.uuid4()),
            "Ce-Specversion": "1.0",
            "Ce-Type": "data.drift.detection",
            "Ce-Source": "datadrift/wine",
            "Ce-Driftresult": str(drift_prediction['data']['is_drift'])
        }
    )

    return response.text, response.status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
