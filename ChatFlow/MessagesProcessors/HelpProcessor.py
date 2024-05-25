from telegram import Update
from telegram.ext import *
from ChatFlow.Core.DialogState import DialogState
from ChatFlow.Core.ProcessorBase import SimpleCommandProcessor
from ChatFlow.MessagesProcessors.CalculateByRuleProcessor import calculateByRuleProcessor, calculateByLastRuleProcessor
from ChatFlow.MessagesProcessors.CreateRuleProcessor import createRuleProcessor
from ChatFlow.MessagesProcessors.DeleteRuleProcessor import deleteRuleProcessor
from ChatFlow.MessagesProcessors.EditRuleProcessor import editRuleProcessor
from ChatFlow.MessagesProcessors.GetRulesProcessor import getRulesProcessor


async def help_command(update: Update, context: CallbackContext, dialog: DialogState) -> None:
    await update.message.reply_text("Чат-бот для сплита зарплаты по счетам.\n"
                              "Доступные команды:\n"
                              f"{getRulesProcessor.GetHelpDescription()}"
                              f"{createRuleProcessor.GetHelpDescription()}"
                              f"{deleteRuleProcessor.GetHelpDescription()}"
                              f"{calculateByLastRuleProcessor.GetHelpDescription()}"
                              f"{editRuleProcessor.GetHelpDescription()}"
                              f"{calculateByRuleProcessor.GetHelpDescription()}")
                              #"/view_requests - просмотреть все запросы\n"
                              #"/add_response - добавить ответ\n"
                              #"/view_responses - просмотреть ответы")

helpProcessor = SimpleCommandProcessor("help", "help", help_command)