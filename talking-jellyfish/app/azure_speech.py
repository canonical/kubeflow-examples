import logging

import azure.cognitiveservices.speech as speechsdk

log = logging.getLogger("Chatbot")


class AzureSpeechRecognition:

    def __init__(self, speech_key, speech_region, language='en-US',
                 use_default_microphone=True, device_name=None):
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region,
            speech_recognition_language=language)

        if use_default_microphone:
            audio_config = speechsdk.audio.AudioConfig(
                use_default_microphone=use_default_microphone)
        else:
            audio_config = speechsdk.audio.AudioConfig(device_name=device_name)

        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config)
        log.debug("AzureSpeechRecognition initialized.")

    def __call__(self, *args, **kwargs):
        log.debug("Listening to the message in mic")
        result_message = self.speech_recognizer.recognize_once_async().get()

        if result_message.reason == speechsdk.ResultReason.RecognizedSpeech:
            result = result_message.text
            log.debug(f"Recognized: {result}")
            return result
        elif result_message.reason == speechsdk.ResultReason.NoMatch:
            log.debug(f"No speech could be recognized:",
                      result_message.no_match_details)
        elif result_message.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result_message.cancellation_details
            log.warning(
                f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                log.error("Error details: {}".format(
                    cancellation_details.error_details))
            raise Exception(cancellation_details.reason)


class AzureSpeechSynthesizer:
    def __init__(self, speech_key, speech_region,
                 voice_name='en-US-JennyNeural', use_default_speaker=True,
                 device_name=None):
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region)
        speech_config.speech_synthesis_voice_name = voice_name

        if use_default_speaker:
            audio_config = speechsdk.audio.AudioOutputConfig(
                use_default_speaker=use_default_speaker)
        else:
            audio_config = speechsdk.audio.AudioOutputConfig(
                device_name=device_name)

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config)
        log.debug("AzureSpeechSynthesizer initialized.")

    def __call__(self, *args, **kwargs):
        text = args[0]
        log.info(f"Synthesis of: {text}")
        result = self.speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            log.debug(f"Speech synthesized for text [{text}]")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            log.debug(
                f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    log.debug(
                        f"Error details: {cancellation_details.error_details}")
            raise Exception(cancellation_details.reason)
