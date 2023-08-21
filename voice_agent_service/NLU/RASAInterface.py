import re
import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
from rasa.model import get_latest_model

logger = logging.getLogger(__name__)

class RASAInterface:
    def __init__(self, model_path: Text):
        self.model_path = get_latest_model(model_path)
        self.agent = Agent.load(self.model_path)

    def preprocess_text(self, text):
        # text to lower case and remove trailing and leading spaces
        preprocessed_text = text.lower().strip()
        # remove special characters, punctuation, and extra whitespaces
        preprocessed_text = re.sub(r'[^\w\s]', '', preprocessed_text).strip()
        return preprocessed_text

    def extract_intent(self, text: Text):
        preprocessed_text = self.preprocess_text(text)
        result = asyncio.run(self.agent.parse_message(preprocessed_text))
        return result
    
    def process_intent(self, intent):
        pass
        # if intent_result['intent']['confidence'] > 0.5:  # You can adjust the confidence threshold as needed
            #     intent = intent_result['intent']['name']
            #     return intent
            # else:
            #     return None