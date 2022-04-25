import uuid

from flask import Flask, request, make_response
import mlflow
import numpy as np
import json

app = Flask(__name__)

loaded_model = mlflow.pyfunc.load_model('./model/')


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

    response = make_response(json.dumps(drift_prediction, cls=NumpyEncoder))
    response.headers["Ce-Id"] = str(uuid.uuid4())
    response.headers["Ce-specversion"] = "0.3"
    response.headers["Ce-Type"] = "data.drift.detection"
    response.headers["Drift-Result"] = drift_prediction['data']['is_drift']

    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
