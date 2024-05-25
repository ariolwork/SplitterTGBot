import random

from ChatFlow.Core.Story import Story, StoryStep
from Splitter.ModelsStorage import MongoStorage
from Splitter.SplitModel import SplitRuleset, SplitRule


class CalculateBySplitStory(Story):
    Split: SplitRuleset

    def __init__(self, ownerId, splitStorage : MongoStorage):
        self.StartStoryMessage = "Начато разбиение по сплиту"
        a3 = CalculateByFoundSplit(None, self)
        a2= DefineTargetSplitToCalculate(a3, self, splitStorage, ownerId)
        self.StorySteps = [a2,a3]
        self.CurrentStep = a2
        self.SplitStorage = splitStorage

class CalculateByLastSplitStory(Story):
    Split: SplitRuleset

    def __init__(self, ownerId, splitStorage: MongoStorage):
        self.Split = splitStorage.GetLastUserSlit(ownerId)
        if self.Split == None:
            self.StartStoryMessage = "Не найдено сплитов для пользователя"
            self.IsTerminated = True
        else:
            self.StartStoryMessage = f"Начато разбиение по последнему сплиту\n{self.Split.GetReadeableDescription()}"
            a3 = CalculateByFoundSplit(None, self)
            self.StorySteps = [a3]
            self.CurrentStep = a3



class DefineTargetSplitToCalculate(StoryStep):
    def getPreStartMessage(self) -> str:
        return "Введите id сплита:"

    def GetNextStep(self):
        if(self.Owner.Split != None):
            return self.NextStep
        return self

    def checkInputForValid(self, message) -> bool:
        try:
            r = int(message)
            return True
        except:
            return False

    def processMessage(self, message):
        exists = self.SplitStorage.GetUserSlit(self.OwnerId, int(message))
        if exists != None:
            self.Owner.Split = exists
            return "Найдет искомый сплит"
        return f"Сплит с id {message} не найден для пользователя"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: CalculateBySplitStory, splitStorage : MongoStorage, ownerId):
        super().__init__(False, nextStep, owner)
        self.SplitStorage = splitStorage
        self.OwnerId = ownerId


class CalculateByFoundSplit(StoryStep):
    splitSucceed = False
    def getPreStartMessage(self) -> str:
        return "Введите сумму для сплита:"

    def GetNextStep(self):
        if self.splitSucceed :
            return None
        return self

    def checkInputForValid(self, message) -> bool:
        try:
            r = float(message)
            return True
        except:
            return False

    def processMessage(self, message):
        self.splitSucceed = True
        summ = float(message)
        return self.Owner.Split.Split(summ)

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: CalculateBySplitStory):
        super().__init__(True, nextStep, owner)