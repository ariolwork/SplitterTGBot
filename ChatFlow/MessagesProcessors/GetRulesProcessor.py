from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from Splitter.ModelsStorage import rulesProvider


async def getRulesForOwner(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    userRules = rulesProvider.GetAllUserSlits(update.message.from_user.id)
    if len(userRules) == 0:
        await update.message.reply_text("Для пользователя еще не зарегистрированно разбиений")
        return
    await update.message.reply_text("\n\n".join([r.GetReadeableDescription() for r in userRules]))

getRulesProcessor = SimpleCommandProcessor("getRules", "Получить все зарегистрированные сплиты" , getRulesForOwner)