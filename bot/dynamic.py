from pymongo import MongoClient
import os

class Dynamic:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGO_ADDRESS'))
        self.db = self.client['kb_dynamic']
    
    def determineReactions(self, message):
        reactions = self.db['reactions'].find_one({"name": "reactions"}, {"name": 0})
        return [reaction for reaction in reactions if any(r in message for r in reactions[reaction])]
    
    # only returning one responce here to prevent 
    def determineResponse(self, message):
        responses = self.db['responses'].find_one({"name": "responses"}, {"name": 0})
        start = [response for response in responses['start'] if any(r in message for r in responses['start'][response])]
        if start:
            return start[0]
        other = [response for response in responses['any'] if any(r in message for r in responses['any'][response])]
        if other:
            return other[0]
        return None
