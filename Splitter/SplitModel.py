import json
import jsonpickle
from datetime import datetime
from json import JSONEncoder


class SplitRuleset:
    def __init__(self, name, setId, ownerId):
        self._id = setId
        self.OwnerId = ownerId
        self.Name = name
        self.Rules = []
        self.CreateDate = str(datetime.now())

    def __dict__(self):
        return dict(
            _id=self._id,
            OwnerId=self.OwnerId,
            Name=self.Name,
            CreateDate=self.CreateDate,
            Rules=json.dumps(jsonpickle.encode(self.Rules))
        )

    @staticmethod
    def FromDict(dict):
        id = dict.get("_id", "Empty")
        ownerId = dict.get("OwnerId", "Empty")
        name = dict.get("Name", "Empty")
        createDate = dict.get("CreateDate", "Empty")
        rules = json.loads(jsonpickle.decode(dict.get("Rules", {})))
        newDict = SplitRuleset(name, id, ownerId)
        newDict.CreateDate = createDate
        newDict.Rules = [SplitRule.FromDict(x) for x in rules]
        return newDict

    def RequiredToFillPercents(self):
        return (1 - sum([i.Percent for i in self.Rules])) * 100

    def Split(self, summ: float):
        sortedRules = sorted(self.Rules, key=lambda x: x.Percent, reverse=True)
        ruleSet = "\n".join([f" - {summ * i.Percent:.2f} - {i.Card} ({i.Percent * 100:.2f}%, {i.Target})" for i in sortedRules])
        return (f"{self.Name} | ID:{self._id} | summ:{summ}\n{ruleSet}")

    def GetReadeableDescription(self, setEnumeration = False):
        if setEnumeration:
            return self.GetReadeableDescriptionWithEnumeration()
        sortedRules = sorted(self.Rules, key=lambda x : x.Percent, reverse=True)
        ruleSet = "\n".join([f" - [ {i.Percent * 100:.2f}% - {i.Target} ({i.Card})]" for i in sortedRules])
        return (f"{self.Name} | ID:{self._id}\n{ruleSet}")

    def GetReadeableDescriptionWithEnumeration(self):
        ruleSet = "\n".join([f" - {ind+1}) [ {i.Percent * 100}% - {i.Target} ({i.Card})]" for ind, i in enumerate(self.Rules)])
        return (f"{self.Name} | ID:{self._id}\n{ruleSet}")


class SplitRule:
    def __init__(self, percent, card, target):
        self.Percent = percent
        self.Card = card
        self.Target = target

    @staticmethod
    def FromDict(dict):
        return SplitRule(
            dict["Percent"],
            dict["Card"],
            dict["Target"]
        )