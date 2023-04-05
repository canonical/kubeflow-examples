import logging

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_DIR = "/app/build/"


class Chatbot(object):

    def __init__(self, model_dir=MODEL_DIR):
        self.log = logging.getLogger()
        self.log.info("Initializing")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir)
        self.chat_history_ids = {}
        self.log.info("Initialized!")

    def predict(self, X, feature_names=[]):
        """
        Return a prediction.
        Parameters
        ----------
        X : array-like
        feature_names : array of feature names (optional)
        """
        self.log.info(f"Predict request: {X}, type: {type(X)}")

        conv_id_column_name = "conversation_id"
        text_column_name = "text"
        conv_id = X[
            feature_names.index(conv_id_column_name) if conv_id_column_name in feature_names else 0]
        text = X[feature_names.index(text_column_name) if text_column_name in feature_names else 1]

        user_input = ''.join(text.tolist()) + self.tokenizer.eos_token

        self.log.debug(f"User input: {user_input}, type: {type(user_input)}")
        user_input_ids = self.tokenizer.encode(user_input, return_tensors='pt')
        self.log.debug(f"user_input_ids: {user_input_ids}")

        conv_history_ids = self.chat_history_ids.get(conv_id)
        self.log.debug(f"conv history ids: {conv_history_ids}")

        bot_input_ids = torch.cat([conv_history_ids, user_input_ids],
                                  dim=-1) if conv_history_ids is not None else user_input_ids

        self.log.debug(f"bot_input_ids: {bot_input_ids}")
        self.chat_history_ids[conv_id] = self.model.generate(
            bot_input_ids, max_length=500,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8)

        response = self.tokenizer.decode(
            self.chat_history_ids[conv_id][:, bot_input_ids.shape[-1]:][0],
            skip_special_tokens=True)

        self.log.info(f"Response: {response}")

        return response
