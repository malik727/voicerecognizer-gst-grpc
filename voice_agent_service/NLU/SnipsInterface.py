import re
from typing import Text
from nlu_inference_agl import SnipsNLUEngine

class SnipsInterface:
    def __init__(self, model_path: Text):
        self.engine = SnipsNLUEngine.from_path(model_path)

    def preprocess_text(self, text):
        # text to lower case and remove trailing and leading spaces
        preprocessed_text = text.lower().strip()
        # remove special characters, punctuation, and extra whitespaces
        preprocessed_text = re.sub(r'[^\w\s]', '', preprocessed_text).strip()
        return preprocessed_text

    def extract_intent(self, text: Text):
        preprocessed_text = self.preprocess_text(text)
        result = self.engine.parse(preprocessed_text)
        return result
    
    def process_intent(self, intent):
        pass
        # if intent_result['intent']:
        #     intent = intent_result['intent']['intentName']
        #     return intent
        # else:
        #     return None