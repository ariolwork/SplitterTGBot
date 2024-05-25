import random

from ChatFlow.Core.Story import Story, StoryStep
from Splitter.ModelsStorage import MongoStorage
from Splitter.SplitModel import SplitRuleset, SplitRule


class EditSplitStory(Story):
    Split: SplitRuleset
    ChangeKind: str
    def __init__(self, ownerId, splitStorage : MongoStorage):
        self.StartStoryMessage = "Редактирование сплита"
        a2 = ChoseEditActionStep(self, splitStorage)
        a1 = GetSplitStep(a2, self, splitStorage, ownerId)
        self.StorySteps = [a1,a2]
        self.CurrentStep = a1
        self.Split = None
        self.SplitStorage = splitStorage



class GetSplitStep(StoryStep):
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
            return f"Найдет искомый сплит\n{self.Owner.Split.GetReadeableDescription(True)}"
        return f"Сплит с id {message} не найден для пользователя"

    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: EditSplitStory, splitStorage : MongoStorage, ownerId):
        super().__init__(False, nextStep, owner)
        self.SplitStorage = splitStorage
        self.OwnerId = ownerId


class ChoseEditActionStep(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Выберите действие редактирования\nE(Extract), M(Merge), S(Save), SA(SaveAsNew), EP(EditPart)"

    def GetNextStep(self):
        return self.NextStep

    def checkInputForValid(self, message) -> bool:
        return message.lower() == "Extract".lower() \
                or message.lower() == "E".lower() \
                or message.lower() == "M".lower() \
                or message.lower() == "Merge".lower() \
                or message.lower() == "S".lower() \
                or message.lower() == "Save".lower() \
                or message.lower() == "SA".lower() \
                or message.lower() == "SaveAsNew".lower() \
                or message.lower() == "EP".lower() \
                or message.lower() == "EditPart".lower()

    def processMessage(self, message: str):
        if message.lower() == "Extract".lower() or message.lower() == "E".lower():
            self.NextStep = ExtractPartSplit(self, self.Owner)
            return "Извлечение % из существующего сплита"
        if message.lower() == "Merge".lower() or message.lower() == "M".lower():
            self.NextStep = MergePartSplit(self, self.Owner)
            return "Объединение двух частей из 1"
        if message.lower() == "Save".lower() or message.lower() == "S".lower():
            self.NextStep = SaveSplit(self.Owner, self.Storage)
            return "Сохранение изменений"
        if message.lower() == "SaveAsNew".lower() or message.lower() == "SA".lower():
            self.NextStep = SaveSplitAsNew(self.Owner, self.Storage)
            return "Сохранение изменений как нового сплита"
        if message.lower() == "EditPart".lower() or message.lower() == "EP".lower():
            self.NextStep = EditPartSplit(self, self.Owner)
            return "Редактирование части"
        return "????. Так не умею"

    def __init__(self, owner: EditSplitStory,  splitStorage: MongoStorage):
        super().__init__(False, None, owner)
        self.Storage = splitStorage


class ExtractPartSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Введите номер части из которой хотите извлечь процент, процент(в формате 0.xx | xx%), Card и Target новой части через | или ,:"

    def GetNextStep(self):
        return self.NextStep

    def checkInputForValid(self, message) -> bool:
        parts = message.replace(',', '|').split('|')
        if len(parts) != 4:
            return False
        return True

    def processMessage(self, message: str):
        parts = message.replace(',', '|').split('|')
        if (parts[1][len(parts[1]) - 1] == '%'):
            percent = float(str(parts[1][:len(parts[1]) - 1]).strip()) * 1.0 / 100
        else:
            percent = float(str(parts[1]).strip())
        numOfPart = int(str(parts[0]))
        if(numOfPart > len(self.Owner.Split.Rules)) or numOfPart <= 0:
            return "Номер части для изменения не корректный"
        editingRule = self.Owner.Split.Rules[numOfPart-1]
        if (editingRule.Percent < percent):
            return "Невозможно извлечь. Процент части меньше извлекаемого"
        editingRule.Percent -= percent
        self.Owner.Split.Rules.append(SplitRule(percent, parts[2].strip(), parts[3].strip()))
        return f"Извлечен процент для сплита. Новый вид\n{self.Owner.Split.GetReadeableDescription(True)}"


    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: EditSplitStory):
        super().__init__(True, nextStep, owner)


class MergePartSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Введите номеа частей которые хотите смерджить, Card и Target новой части через | или ,:"

    def GetNextStep(self):
        return self.NextStep

    def checkInputForValid(self, message) -> bool:
        parts = message.replace(',', '|').split('|')
        if len(parts) > 2:
            return True
        return False

    def processMessage(self, message: str):
        parts = message.replace(',', '|').split('|')
        sumPercent = 0
        for i in range(0, len(parts)-2):
            numOfPart = int(str(parts[i]))
            if (numOfPart > len(self.Owner.Split.Rules)) or numOfPart <= 0:
                return f"Номер части {numOfPart} не корректный"
        for i in range(0, len(parts) - 2):
            numOfPart = int(str(parts[0]))
            editingRule = self.Owner.Split.Rules[numOfPart-1]
            sumPercent += editingRule.Percent
            self.Owner.Split.Rules.remove(editingRule)
        self.Owner.Split.Rules.append(SplitRule(sumPercent, parts[len(parts)-2].strip(), parts[len(parts)-1].strip()))
        return f"Объединены части сплита. Новый вид\n{self.Owner.Split.GetReadeableDescription(True)}"


    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: EditSplitStory):
        super().__init__(True, nextStep, owner)


class EditPartSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Введите номер части которую хотите изменить, Card и Target части через | или ,:"

    def GetNextStep(self):
        return self.NextStep

    def checkInputForValid(self, message) -> bool:
        parts = message.replace(',', '|').split('|')
        if len(parts) == 3:
            return True
        return False

    def processMessage(self, message: str):
        parts = message.replace(',', '|').split('|')

        numOfPart = int(str(parts[0]))
        if (numOfPart > len(self.Owner.Split.Rules)) or numOfPart <= 0:
            return f"Номер части {numOfPart} не корректный"
        editingRule = self.Owner.Split.Rules[numOfPart-1]
        editingRule.Target = str(parts[1])
        editingRule.Card = str(parts[2])
        return f"Изменена часть сплита. Новый вид\n{self.Owner.Split.GetReadeableDescription(True)}"


    def checkForCancelStory(self, message) -> bool:
        return False

    def __init__(self, nextStep, owner: EditSplitStory):
        super().__init__(True, nextStep, owner)



class SaveSplit(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Подтвердите сохранение сплита\n{self.Owner.Split.GetReadeableDescription(True)}\n --y-- || --n--"

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
        return True

    def __init__(self, owner: EditSplitStory, splitStorage: MongoStorage):
        super().__init__(True, None, owner)
        self.Storage = splitStorage


class SaveSplitAsNew(StoryStep):
    def getPreStartMessage(self) -> str:
        return f"Подтвердите сохранение сплита как нового\n{self.Owner.Split.GetReadeableDescription(True)}\n --y-- || --n--"

    def GetNextStep(self):
        return None

    def checkInputForValid(self, message) -> bool:
        return True

    def processMessage(self, message: str):
        if message == "Y" or message == "y":
            self.Owner.Split._id = random.randint(0,1000000)
            self.Storage.AddNewSplit(self.Owner.Split)
            return "Сплит сохранен"
        return "Создание сплита отменено"

    def checkForCancelStory(self, message) -> bool:
        return True

    def __init__(self, owner: EditSplitStory, splitStorage: MongoStorage):
        super().__init__(True, None, owner)
        self.Storage = splitStorage