from Splitter.SplitModel import SplitRuleset, SplitRule
from pymongo import MongoClient
import os

#_ruleStorage = []
#newRuleset = SplitRuleset(1, "ArtemsTest", 1)
#_ruleStorage.append(newRuleset)
#newRuleset.Rules = [SplitRule(0.6, "A", "B"), SplitRule(0.4, "A", "C")]
class MongoStorage:
    def __init__(self):
        CONNECTION_STRING = f"mongodb://{str(os.getenv('DB'))}/SampleDB"
        client = MongoClient(CONNECTION_STRING)
        self.db = client['salary_split']

    def GetAllUserSlits(self, ownerId):
        splits = self.db[str(ownerId)]
        item_details = splits.find({"OwnerId" : ownerId})
        return [SplitRuleset.FromDict(x) for x in item_details]

    def GetLastUserSlit(self, ownerId):
        splits = self.db[str(ownerId)]
        item_details = splits.find_one({"OwnerId": ownerId}, sort=[("CreateDate", -1)])
        return SplitRuleset.FromDict(item_details)

    def GetUserSlit(self, ownerId, id):
        splits = self.db[str(ownerId)]
        item_details = splits.find({"OwnerId": ownerId, "_id": id})
        result = [SplitRuleset.FromDict(x) for x in item_details]
        if len(result) > 0:
            return result[0]
        return None

    def DeleteUserSlit(self, ownerId, id):
        splits = self.db[str(ownerId)]
        splits.delete_one({"OwnerId" : ownerId, "_id": id})


    def AddNewSplit(self, newSplit: SplitRuleset):
        splits = self.db[str(newSplit.OwnerId)]
        r = newSplit.__dict__()
        splits.insert_one(r)


rulesProvider = MongoStorage()