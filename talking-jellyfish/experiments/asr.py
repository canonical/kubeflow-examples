from transformers import pipeline
from datasets import load_dataset

dataset = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
dataset = dataset.sort("id")
audio_file = dataset[0]["audio"]["path"]

speech_recognizer = pipeline(task="automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
res = speech_recognizer(audio_file)

print(res)