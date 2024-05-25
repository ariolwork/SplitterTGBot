from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from ChatFlow.UserStory.CalculateBySplitStory import CalculateBySplitStory, CalculateByLastSplitStory
from Splitter.ModelsStorage import rulesProvider


async def calculateByRule(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    dialog.ActiveUserStory = CalculateBySplitStory(dialog.OwnerId, rulesProvider)
    await update.message.reply_text(f"{dialog.ActiveUserStory.StartStoryMessage}\n{dialog.ActiveUserStory.CurrentStep.getPreStartMessage()}")

calculateByRuleProcessor = SimpleCommandProcessor("calculateByRule", "Посчитать по конкретному сплиту" , calculateByRule)



async def calculateByLastRule(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    dialog.ActiveUserStory = CalculateByLastSplitStory(dialog.OwnerId, rulesProvider)
    if dialog.ActiveUserStory.CurrentStep != None:
        await update.message.reply_text(f"{dialog.ActiveUserStory.StartStoryMessage}\n{dialog.ActiveUserStory.CurrentStep.getPreStartMessage()}")
    else:
        await update.message.reply_text(
            f"{dialog.ActiveUserStory.StartStoryMessage}")
calculateByLastRuleProcessor = SimpleCommandProcessor("calculateByLastRule", "Посчитать по последнему сплиту" , calculateByLastRule)