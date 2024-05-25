from abc import abstractmethod


class StoryStep:
    validated: bool
    @abstractmethod
    def getPreStartMessage(self) -> str:
        pass

    @abstractmethod
    def checkForCancelStory(self, message) -> bool:
        pass

    @abstractmethod
    def processMessage(self, message):
        pass

    @abstractmethod
    def checkInputForValid(self, message) -> bool:
        pass

    @abstractmethod
    def GetNextStep(self):
        pass

    def GetBaseNextStep(self):
        if(self.validated):
            return self.GetNextStep()
        return self

    def process(self, message):
        if self.checkInputForValid(message) == False:
            self.validated = False
            return "Validate of message not passed"
        self.validated = True
        result = self.processMessage(message)
        self.checkForCancelStory(message)
        return result

    def __init__(self, isterminate, nextStep, owner):
        self.IsTerminated = isterminate
        self.NextStep = nextStep
        self.Owner = owner

class Story:
    StorySteps = []
    CurrentStep : StoryStep = None
    StartStoryMessage = ""
    IsTerminated = False

    def StartStory(self):
        self.CurrentStep = self.StorySteps[0]
        return f"{self.StartStoryMessage}\n<c> to cancel"

    def ProcessMessage(self, message):
        result = ""
        try:
            result = self.CurrentStep.process(message)
            prevStep = self.CurrentStep
            self.CurrentStep = self.CurrentStep.GetBaseNextStep()
            if(self.CurrentStep == None):
                self.IsTerminated = True
            if prevStep != self.CurrentStep and self.CurrentStep != None:
                result = f"{result}\n{self.CurrentStep.getPreStartMessage()}"
        except Exception:
            result = "Что то пошло не так. Попробуйте еще раз"
        return result
