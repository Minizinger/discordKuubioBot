import json
import os
import re
from emoji import UNICODE_EMOJI
import codecs

class Config:
    def __init__(self):
        with codecs.open('../config/reactions.json', 'r', 'utf-8') as f:
            self.reactions = json.load(f)
        with codecs.open('../config/responses.json', 'r', 'utf-8') as f:
            self.responses = json.load(f)
    
    def determine_reactions(self, message):
        return [reaction for reaction in self.reactions if any(re.search(r, message) if r in UNICODE_EMOJI else re.search(r'\b' + r + r'\b', message) for r in self.reactions[reaction])]
    
    # only returning one responce here to prevent 
    def determine_response(self, message):
        start = [response for response in self.responses['start'] if any(re.search(r'\A' + r + r'\b', message) for r in self.responses['start'][response])]
        if start:
            return start[0]
        other = [response for response in self.responses['any'] if any(r in message for r in self.responses['any'][response])]
        if other:
            return other[0]
        return None
