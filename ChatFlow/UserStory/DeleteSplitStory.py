import random

from ChatFlow.Core.Story import Story, StoryStep
from Splitter.ModelsStorage import MongoStorage
from Splitter.SplitModel import SplitRuleset, SplitRule


class DeleteSplitStory(Story):
    Split: SplitRuleset

    def __init__(self, ownerId, splitStorage : MongoStorage):
        self.StartStoryMessage = "Удаление сплита"
        a2 = DeleteSplit(None, self, splitStorage)
        a1 = GetSplitToDeleteStep(a2, self, splitStorage, ownerId)
        self.StorySteps = [a1,a2]
        self.CurrentStep = a1
        self.SplitStorage = splitStorage



class GetSplitToDeleteStep(StoryStep):
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
        id = int(message)
        exists = self.SplitStorage.GetUserSlit(self.OwnerId, id)
        if exists != None:
            self.Owner.Split = exists
            return "Найдет искомый сплит"
        return f"Сплит с id {message} не найден для пользователя"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: DeleteSplitStory, splitStorage : MongoStorage, ownerId):
        super().__init__(False, nextStep, owner)
        self.SplitStorage = splitStorage
        self.OwnerId = ownerId


class DeleteSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Подтвердите удаление сплита\n{self.Owner.Split.GetReadeableDescription()}\n --y-- || --n--"

    def GetNextStep(self):
        return None

    def checkInputForValid(self, message) -> bool:
        return True

    def processMessage(self, message: str):
        if message == "Y" or message == "y":
            self.Storage.DeleteUserSlit(self.Owner.Split.OwnerId, self.Owner.Split._id)
            return "Сплит удален"
        return "Удаление сплита отменено"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: DeleteSplitStory, splitStorage: MongoStorage):
        super().__init__(True, nextStep, owner)
        self.Storage = splitStorage