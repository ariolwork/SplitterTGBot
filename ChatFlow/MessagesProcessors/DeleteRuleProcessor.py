from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from ChatFlow.UserStory.DeleteSplitStory import DeleteSplitStory
from Splitter.ModelsStorage import rulesProvider


async def deleteRule(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    dialog.ActiveUserStory = DeleteSplitStory(dialog.OwnerId, rulesProvider)
    await update.message.reply_text(f"{dialog.ActiveUserStory.StartStoryMessage}\n{dialog.ActiveUserStory.CurrentStep.getPreStartMessage()}")
deleteRuleProcessor = SimpleCommandProcessor("deleteRule", "Удалить сплин" , deleteRule)