import json
import logging
import os
import time
import uuid

import requests

from azure_speech import AzureSpeechRecognition, AzureSpeechSynthesizer
from config import SyncConfig

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ChatbotApp")


def chatbot(conv_id, text):
    body = {
        "data": {
            "ndarray": [conv_id, text]
        }
    }
    response = requests.post(CHATBOT_ENDPOINT, json=body)
    log.debug(response.status_code, response.content)
    return json.loads(response.content)["strData"]


def init_speech_services():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    log.debug("Environment properties set")
    use_default_microphone = bool(os.getenv("CHATBOT_USE_DEFAULT_MICROPHONE", True))
    microphone_device_name = os.getenv("CHATBOT_MICROPHONE_DEVICE_NAME", None)
    recognition = AzureSpeechRecognition(speech_key, speech_region,
                                         use_default_microphone=use_default_microphone,
                                         device_name=microphone_device_name)
    log.debug("Speech recognition API set")

    use_default_speaker = bool(os.getenv("CHATBOT_USE_DEFAULT_SPEAKER", True))
    speaker_device_name = os.getenv("CHATBOT_SPEAKER_DEVICE_NAME", None)
    synthesizer = AzureSpeechSynthesizer(speech_key, speech_region,
                                         use_default_speaker=use_default_speaker,
                                         device_name=speaker_device_name)
    log.debug("Speech synthesizer API set")
    return recognition, synthesizer


if __name__ == '__main__':

    CONFIG_FILE = os.getenv("JELLYFISH_CONFIG_SYNC_FILENAME",
                            "/tmp/jellyfish-sync.conf")
    config = SyncConfig(CONFIG_FILE)
    config.save_config(cv=False, chat=False)
    log.info(f"SyncConfig file created with values: {config}")

    CHATBOT_ENDPOINT = os.getenv("CHATBOT_ENDPOINT")

    speech_recognition, speech_synthesizer = init_speech_services()

    result_text = None
    conversation_id = None
    while result_text != "Execute order 66.":
        if config.cv:
            log.info("Initiate the conversation.")
            config.save_config(cv=False, chat=True)
            conversation_id = str(uuid.uuid4())
            INITIATION_TEXT = "Hello, would you like to talk with me?"
            speech_synthesizer(INITIATION_TEXT)
            log.info(f"New person welcomed using text: {INITIATION_TEXT}, conv_id: {conversation_id}")
        elif config.chat:
            log.info("Speak to the microphone")
            result_text = speech_recognition()

            if result_text:
                log.info(f"Send user text to chatbox: {result_text}, conv_id: {conversation_id}")
                chatbot_replay = chatbot(conversation_id, result_text)
                log.info(f"Chatbot reply: {chatbot_replay}")
                speech_synthesizer(chatbot_replay)
                log.info(f"Chatbot reply synthesized into sound.")
            else:
                log.info("No human speech sound was detected.")
                config.save_config(cv=False, chat=False)

        else:
            log.debug("Waiting for new person to arrive.")
            time.sleep(1)
            config.load_config()

    log.info("Order 66 executed. Jedi were eliminated. Shutting off.")
