from loguru import logger

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler

from mailing_bot.shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT, \
    GET_MAIN_MENU_INDICATORS, \
    GET_GROUP_DETAILING_NPS_BUTTON, \
    GET_GRADE_INFO_BUTTON, \
    GET_SEMESTERS_DETAILING_BUTTON, \
    GET_PREV_SEM_DETAILING, \
    GET_NEXT_SEM_DETAILING
from mailing_bot.shp_mailing_bot.handlers import get_prep_indicators, grade_info, group_detailing_nps, \
    knowledge_base_link, semester_detailing, main_menu

logger.add('debug.log', encoding='utf8', rotation='10 MB', compression='zip')
preps_cashed_list = None


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
    update.message.reply_text('Не уверен, что понятийно 🥺\nЯ ещё не очень хорошо говорить русски, я молодой бот')


def init_dispatcher(updater: Update):
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_action))
    # команда старта

    dispatcher.add_handler(CommandHandler('help', help_action))
    # команда help -- ссылка на ответственного за бота (настраивается в конфиге)

    dispatcher.add_handler(CommandHandler('get_indicators', get_prep_indicators.get_indicators_action))
    # получение показателей

    dispatcher.add_handler(CommandHandler('knowledge_base', knowledge_base_link.get_kd_link_action))
    # получение ссылки на БЗ

    dispatcher.add_handler(CallbackQueryHandler(main_menu.main_menu_indicators_action,
                                                pattern=GET_MAIN_MENU_INDICATORS))
    # кнопка, которая используется, когда преп ушел в какое-то ответвление (типа детализации посеместрам и т.д.)

    dispatcher.add_handler(CallbackQueryHandler(group_detailing_nps.get_group_detailing_nps_action,
                                                pattern=GET_GROUP_DETAILING_NPS_BUTTON))
    # кнопка детализации по группам

    dispatcher.add_handler(CallbackQueryHandler(grade_info.get_grade_info_action,
                                                pattern=GET_GRADE_INFO_BUTTON))
    # кнопка получения информации о формировании грейда

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.get_nps_stat,
                                                pattern=GET_SEMESTERS_DETAILING_BUTTON))
    # кнопка получения статистики по NPS (кидает на последний сем)

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.get_nps_stat_prev,
                                                pattern=GET_PREV_SEM_DETAILING))

    dispatcher.add_handler(CallbackQueryHandler(semester_detailing.get_nps_stat_next,
                                                pattern=GET_NEXT_SEM_DETAILING))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_action))
    # обработка остальных сообщений

    logger.info('Диспетчер запросов успешно инициализирован.')


def init_prep_list():
    global preps_cashed_list
