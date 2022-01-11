from loguru import logger
from random import choice

from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler, Handler

import mailing_bot.shp_mailing_bot.config as config
from mailing_bot.shp_mailing_bot.handlers import get_prep_indicators, grade_info, group_detailing_nps, \
    knowledge_base_link, semester_detailing, main_menu

logger.add('debug.log', encoding='utf8', rotation='10 MB', compression='zip')


def start_action(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    logger.info(f'Отправлено сообщение старта пользователю {user.name}')

    update.message.reply_text(f'Здравствуйте, {user.first_name}')

    keyboard_markup = None
    update.message.reply_text('Выберите действие в меню или введите "/"',
                              reply_markup=keyboard_markup)




def undefined_message_action(update: Update, context: CallbackContext):
    update.message.reply_text('Не уверен, что понятийно 🥺\nЯ ещё не очень хорошо говорить русски, я молодой бот')


def init_dispatcher(updater: Update):
    logger.debug('Ининциализация диспетчера запросов')
    dispatcher = updater.dispatcher

    logger.debug('Добавление команды /start')
    dispatcher.add_handler(CommandHandler('start', start_action))

    logger.debug('Добавление команды /get_indicators')
    dispatcher.add_handler(CommandHandler('get_indicators', get_prep_indicators.get_indicators_action))

    logger.debug('Добавление команды /knowledge_base')
    dispatcher.add_handler(CommandHandler('knowledge_base', knowledge_base_link.get_kd_link_action))

    dispatcher.add_handler(CallbackQueryHandler(main_menu.main_menu_indicators_action,
                                                pattern=config.GET_MAIN_MENU_INDICATORS))

    dispatcher.add_handler(CallbackQueryHandler(group_detailing_nps.get_group_detailing_nps_action,
                                                pattern=config.GET_GROUP_DETAILING_NPS_BUTTON))

    dispatcher.add_handler(CallbackQueryHandler(grade_info.get_grade_info_action,
                                                pattern=config.GET_GRADE_INFO_BUTTON))

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.i_21_22_sem_nps,
                                                pattern=semester_detailing.I_21_22_SEM))

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.ii_20_21_sem_nps,
                                                pattern=semester_detailing.II_20_21_SEM))

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.i_20_21_sem_nps,
                                                pattern=semester_detailing.I_20_21_SEM))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_action))

    logger.info('Диспетчер запросов успешно инициализирован')
