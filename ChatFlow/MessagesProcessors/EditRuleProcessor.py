from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from ChatFlow.UserStory.DeleteSplitStory import DeleteSplitStory
from ChatFlow.UserStory.EdiitSplitStory import EditSplitStory
from Splitter.ModelsStorage import rulesProvider


async def editRule(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    dialog.ActiveUserStory = EditSplitStory(dialog.OwnerId, rulesProvider)
    await update.message.reply_text(f"{dialog.ActiveUserStory.StartStoryMessage}\n{dialog.ActiveUserStory.CurrentStep.getPreStartMessage()}")
editRuleProcessor = SimpleCommandProcessor("editRule", "Редактировать сплит" , editRule)