from abc import abstractmethod

from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState

class CommandProcessor:
    Name: str

    def __init__(self, nameC: str, decription):
        self.Name = nameC
        self.Decription = decription

    @abstractmethod
    async def Process(self, update: Update, context: CallbackContext, dialog: DialogState):
        pass

    def GetHelpDescription(self):
        return str("/{} - {}\n".format(self.Name, self.Decription))

class SimpleCommandProcessor(CommandProcessor):
    def __init__(self, nameC: str, decription, handler):
        super().__init__(nameC, decription)
        self.Processor = handler

    async def Process(self, update: Update, context: CallbackContext, dialog: DialogState):
        await self.Processor(update, context, dialog)



