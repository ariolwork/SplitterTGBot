from telegram.ext import *

from ChatFlow.Core.DialogState import DialogsContaner
from ChatFlow.MessagesProcessors.CalculateByRuleProcessor import calculateByRuleProcessor, calculateByLastRuleProcessor
from ChatFlow.MessagesProcessors.CreateRuleProcessor import createRuleProcessor
from ChatFlow.MessagesProcessors.DeleteRuleProcessor import deleteRuleProcessor
from ChatFlow.MessagesProcessors.EditRuleProcessor import editRuleProcessor
from ChatFlow.MessagesProcessors.GetRulesProcessor import getRulesProcessor
from ChatFlow.MessagesProcessors.HelpProcessor import helpProcessor
from ChatFlow.MessagesProcessors.messageProcessor import messageProcessor

import os

# Токен бота, полученный от BotFather в Telegram
TOKEN = str(os.getenv('TG'))

# хранилище состояний чата
# определитель обработчика комманды с контекстом
_dialogsContaner = DialogsContaner()


def command_processor_wrapper(processor):
    async def caller( update, context) : var = {
        await processor(update, context, _dialogsContaner.GetOrAddDialog(update.message.from_user.id))
    }
    return caller


# Создание и настройка бота
def main() -> None:
    dispatcher = Application.builder().token(TOKEN).build()
    dispatcher.add_handler(CommandHandler(helpProcessor.Name, command_processor_wrapper(helpProcessor.Process)))
    dispatcher.add_handler(CommandHandler(getRulesProcessor.Name, command_processor_wrapper(getRulesProcessor.Process)))
    dispatcher.add_handler(CommandHandler(createRuleProcessor.Name, command_processor_wrapper(createRuleProcessor.Process)))
    dispatcher.add_handler(CommandHandler(deleteRuleProcessor.Name, command_processor_wrapper(deleteRuleProcessor.Process)))
    dispatcher.add_handler(CommandHandler(calculateByRuleProcessor.Name, command_processor_wrapper(calculateByRuleProcessor.Process)))
    dispatcher.add_handler(CommandHandler(calculateByLastRuleProcessor.Name, command_processor_wrapper(calculateByLastRuleProcessor.Process)))
    dispatcher.add_handler(CommandHandler(editRuleProcessor.Name, command_processor_wrapper(editRuleProcessor.Process)))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_processor_wrapper(messageProcessor.Process)))
    dispatcher.run_polling()

if __name__ == '__main__':
    main()