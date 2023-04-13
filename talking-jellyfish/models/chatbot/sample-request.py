import uuid

from Chatbot import Chatbot


def chatbox_over_http(conv_id, text):
    import requests
    MODEL_ENDPOINT = "http://10.152.183.140:8000"
    body = {
        "data": {
            "ndarray": [conv_id, text]
        }
    }
    return requests.post(MODEL_ENDPOINT + "/api/v0.1/predictions", json=body)


# Local model execution
model = Chatbot("./build")
conv_id = str(uuid.uuid4())

for step in range(10):
    user_input = input(f">> User {step}:")

    # res = model.predict(np.array([conv_id, user_input]), ["conversation_id", "text"])
    # print(res)

    res = chatbox_over_http(conv_id, user_input)
    print(res.status_code, res.text)
