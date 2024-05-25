from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from ChatFlow.UserStory.AddNewSplitStory import NewSplitStory
from Splitter.ModelsStorage import rulesProvider


async def createRule(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    dialog.ActiveUserStory = NewSplitStory(dialog.OwnerId, rulesProvider)
    await update.message.reply_text(f"{dialog.ActiveUserStory.StartStoryMessage}\n{dialog.ActiveUserStory.CurrentStep.getPreStartMessage()}")

createRuleProcessor = SimpleCommandProcessor("createRule", "Создать сплин" , createRule)