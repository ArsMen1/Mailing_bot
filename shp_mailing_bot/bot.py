
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler

import mailing_bot.shp_mailing_bot.handlers.get_prep_indicators_semester_navigation
from mailing_bot.logger_bot import logger
from mailing_bot.shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT, GET_CURR_SEM, GET_NEXT_SEM, GET_PREV_SEM

from mailing_bot.shp_mailing_bot.handlers import get_prep_indicators_main, knowledge_base_link


def start_action(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    logger.info(f'Отправлено сообщение старта пользователю {user.name}')

    update.message.reply_text(f'Здравствуйте, {user.first_name}')

    keyboard_markup = None
    update.message.reply_text('Выберите действие в меню или введите "/"',
                              reply_markup=keyboard_markup)


def help_action(update: Update, context: CallbackContext):
    keyboard_markup = None
    update.message.reply_text(
        'Если вы столкнулись с проблемой, связанной со мной, '
        'чувствуете злость, негодование, обиду, презрение или просто растерянность, '
        'вдохните и выдохните на 10 счётов 🧘 \n\n'
        f'А потом напишите {RESPONSIBLE_FOR_THE_BOT}. \nЭто моя мама, она будет рада обратной связи.',
        reply_markup=keyboard_markup)


def undefined_message_action(update: Update, context: CallbackContext):
    update.message.reply_text('Не уверен, что понятийно 🥺\n'
                              'Я ещё не очень хорошо говорить русски, я молодой бот. \n'
                              'Используйтэ команда с "/"')


def init_dispatcher(updater: Update):
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_action))
    # команда старта

    dispatcher.add_handler(CommandHandler('help', help_action))
    # команда help -- ссылка на ответственного за бота (настраивается в конфиге)

    dispatcher.add_handler(CommandHandler('get_indicators', get_prep_indicators_main.get_indicators_action))
    # получение показателей текущего семестра

    dispatcher.add_handler(CallbackQueryHandler(
        mailing_bot.shp_mailing_bot.handlers.get_prep_indicators_semester_navigation.get_prev_sem_indicators_action,
        pattern=GET_PREV_SEM))
    # получение показателей следующего семестра

    dispatcher.add_handler(CallbackQueryHandler(
        mailing_bot.shp_mailing_bot.handlers.get_prep_indicators_semester_navigation.get_next_sem_indicators_action,
        pattern=GET_NEXT_SEM))
    # получение показателей предыдущего семестра

    dispatcher.add_handler(CommandHandler('knowledge_base', knowledge_base_link.get_kd_link_action))
    # получение ссылки на БЗ

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_action))
    # обработка остальных сообщений

    logger.info('Диспетчер запросов успешно инициализирован.')
