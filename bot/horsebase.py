#horsebase = database for storing horses
from pymongo import MongoClient
import operator
import os
import datetime

class HorseBase:
    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGO_ADDRESS', ''))
        self.db = self.client['kuubiobot']

    def addHorseToDB(self, channel, time, poster):
        horse = {'time': time, 'author': poster}
        self.db[channel].insert_one(horse)

    def getMyHorses(self, channel, poster):
        total = self.db[channel].find({'author': poster}).count()
        month = self.db[channel].find({'author': poster, 'time': {'$gte': datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)}}).count()
        return {'total': total, 'month': month}

    def getTopHorses(self, channel, topPositions):
        AlltimeTop = []
        authors = self.db[channel].distinct('author')
        horsesperauthor = {}
        for a in authors:
            horsesperauthor[a] = self.db[channel].find({'author': a}).count()
        if len(authors) > 0:
            for _ in range(topPositions):
                if len(horsesperauthor) == 0:
                    break
                topresult = max(horsesperauthor.items(), key=operator.itemgetter(1))
                AlltimeTop.append(topresult)
                del horsesperauthor[topresult[0]]
        
        MonthTop = []
        authors = self.db[channel].distinct('author', {'time': {'$gte': datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)}})
        horsesperauthor = {}
        for a in authors:
            horsesperauthor[a] = self.db[channel].find({'author': a, 'time': {'$gte': datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)}}).count()
        if len(authors) > 0:
            for _ in range(topPositions):
                if len(horsesperauthor) == 0:
                    break
                topresult = max(horsesperauthor.items(), key=operator.itemgetter(1))
                MonthTop.append(topresult)
                del horsesperauthor[topresult[0]]

        return {'alltime': AlltimeTop, 'month': MonthTop}

    def getTotalHorses(self, channel):
        return self.db[channel].find().count()