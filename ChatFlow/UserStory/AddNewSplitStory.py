import random

from ChatFlow.Core.Story import Story, StoryStep
from Splitter.ModelsStorage import MongoStorage
from Splitter.SplitModel import SplitRuleset, SplitRule


class NewSplitStory(Story):
    Split: SplitRuleset

    def __init__(self, ownerId, splitStorage: MongoStorage):
        self.Split = SplitRuleset("", random.randint(0,1000000) , ownerId)
        self.StartStoryMessage = "Начато добавление нового разбиения"
        a3 = SaveSplit(None, self, splitStorage)
        a2= SetSplitPartStep(a3, self)
        a1 = InitNewSplitStep(a2, self)
        self.StorySteps = [a1,a2,a3]
        self.CurrentStep = a1
        self.SplitStorage = splitStorage



class InitNewSplitStep(StoryStep):
    def getPreStartMessage(self) -> str:
        return "Введите имя для сплита:"

    def GetNextStep(self):
        return self.NextStep

    def checkInputForValid(self, message) -> bool:
        if len(message) > 64:
            return False
        return True

    def processMessage(self, message):
        self.Owner.Split.Name = message
        return f"Создан новый сплит с именем {message}"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: NewSplitStory):
        super().__init__(False, nextStep, owner)


class SetSplitPartStep(StoryStep):
    def getPreStartMessage(self) -> str:
        return ("Введите часть сплита в одном из форматов:\n"
                "[aa%, cardName, target]\n"
                "[aa% | cardName | target]\n"
                "[0.aa, cardName, target]\n"
                "[0.aa | cardName | target]\n")

    def GetNextStep(self):
        if abs(self.Owner.Split.RequiredToFillPercents()) < 0.001:
            return self.NextStep
        return self

    def checkInputForValid(self, message) -> bool:
        parts = message.replace(',', '|').split('|')
        if len(parts) != 3:
            return False
        return True

    def processMessage(self, message: str):
        parts = message.split(',')
        if(parts[0][len(parts[0])-1] == '%'):
            percent = float(str(parts[0][:len(parts[0])-1]).strip())*1.0/100
        else:
            percent = float(str(parts[0]).strip())
        self.Owner.Split.Rules.append(SplitRule(percent, parts[1].strip(), parts[2].strip()))
        if abs(self.Owner.Split.RequiredToFillPercents()) < 0.001:
            return "Все части введены"
        return f"Добавлена часть. Осталось {self.Owner.Split.RequiredToFillPercents()}%"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: NewSplitStory):
        super().__init__(False, nextStep, owner)

class SaveSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Подтвердите создание сплита\n{self.Owner.Split.GetReadeableDescription()}\n --y-- || --n--"

    def GetNextStep(self):
        return None

    def checkInputForValid(self, message) -> bool:
        return True

    def processMessage(self, message: str):
        if message == "Y" or message == "y":
            self.Storage.AddNewSplit(self.Owner.Split)
            return "Сплит сохранен"
        return "Создание сплита отменено"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: NewSplitStory, splitStorage: MongoStorage):
        super().__init__(True, nextStep, owner)
        self.Storage = splitStorage