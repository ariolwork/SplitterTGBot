from ChatFlow.Core.Story import Story


class DialogState:
    ActiveUserStory: Story = None

    def __init__(self, ownerId):
        self.OwnerId = ownerId

    def Process(self, message):
        if message == 'c' or message == 'C':
            if self.ActiveUserStory != None:
                self.ActiveUserStory = None
                return "Активная стори сброшена"
            return "Нат активных стори"
        if self.ActiveUserStory != None:
            result = self.ActiveUserStory.ProcessMessage(message)
            if(self.ActiveUserStory.IsTerminated):
                self.ActiveUserStory = None
            return result
        return "There are no any of active stories"

    def SetNewUserStory(self, story):
        self.ActiveUserStory = story

class DialogsContaner:
    dialogs = {}

    def GetOrAddDialog(self, ownerId):
        if ownerId in self.dialogs.keys():
            return self.dialogs[ownerId]
        newOwnedDialog = DialogState(ownerId)
        self.dialogs[ownerId] = newOwnedDialog
        return newOwnedDialog

