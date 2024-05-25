from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor


async def new_message(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    await update.message.reply_text(dialog.Process(update.message.text))

messageProcessor = SimpleCommandProcessor("","", new_message)