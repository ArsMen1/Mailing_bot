import mailing_bot.shp_mailing_bot.config as config
from random import choice
from time import sleep

from loguru import logger

from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler, Handler

from mailing_bot.shp_mailing_bot.config import CNC_SPREADSHEET_CELLS_RANGE, CNC_SPREADSHEET_ID, INDICATORS_SHEET_ID, \
    INDICATORS_LIST
from mailing_bot.shp_mailing_bot.google_auth import authorize

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')

GET_KD_LINK_BUTTON = "База знаний"

GET_INDICATORS_BUTTON = "Мои показатели"

GET_MAIN_MENU_INDICATORS = "Главное меню"
GET_CURR_NPS_DETAILING_BUTTON = "Детализация NPS"
GET_SEMESTERS_DETAILING_BUTTON = "Детализация по семестрам"
GET_GRADE_INFO_BUTTON = "Грейд"


def get_values_from_sheet() -> list:
    service = authorize()

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=INDICATORS_SHEET_ID, range=f'{INDICATORS_LIST}!A2:D1000').execute()
    values = result.get('values', [])
    return values


def get_prep_indicators(values: list, prep_id: int) -> tuple:  # table info parser
    # getting average info
    average_nps = values[0][2]
    average_retirement = values[0][3]

    # getting prep info
    for prep_info in values:
        if len(prep_info) == 3:
            if prep_info[1].isdigit() and int(prep_info[1]) == prep_id:  # find user indicators
                nps = prep_info[2]
                retirement = 0
                return nps, retirement, average_nps, average_retirement
        elif len(prep_info) == 4:
            if prep_info[1].isdigit() and int(prep_info[1]) == prep_id:  # find user indicators
                nps = prep_info[2]
                retirement = prep_info[3]
                return nps, retirement, average_nps, average_retirement
    return 0, 0, 0, 0


def evaluation_indicator(nps: str = None, retirement: str = None) -> str:  # get comment for nps or retirement
    if nps and nps[-1] == "%":
        nps = float(nps.replace(",", ".")[:-1])
    if retirement and retirement[-1] == "%":
        retirement = float(retirement.replace(",", ".")[:-1])

    if (nps and nps >= config.TOP_BAR_NPS) or \
            (retirement and retirement >= config.TOP_BAR_RETIREMENT):
        return choice(config.EXCELLENT_INDICATORS_COMMENTS)

    elif (nps and config.MEDIUM_BAR_NPS <= nps < config.TOP_BAR_NPS) or \
            (retirement and config.MEDIUM_BAR_RETIREMENT <= retirement <= config.TOP_BAR_RETIREMENT):
        return choice(config.GOOD_INDICATORS_COMMENTS)

    elif (nps and nps < config.MEDIUM_BAR_NPS) or \
            (retirement and retirement < config.MEDIUM_BAR_RETIREMENT):
        return choice(config.BAD_INDICATORS_COMMENTS)


def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    logger.info(f"Отправлено сообщение старта пользователю {user.name}")

    update.message.reply_text(
        f'Здравствуйте, {user.first_name} 🙂')

    keyboard_start = [
        [
            KeyboardButton(GET_INDICATORS_BUTTON),
            KeyboardButton(GET_KD_LINK_BUTTON)
        ]
    ]
    keyboard_markup = ReplyKeyboardMarkup(keyboard=keyboard_start, resize_keyboard=True)
    update.message.reply_text("Выберите действие", reply_markup=keyboard_markup)


def get_kd_link_action(update: Update, context: CallbackContext) -> None:  # get knowledge base link button
    keyboard = [
        [
            InlineKeyboardButton("База Знаний", url=config.KNOWLEDGE_BASE_LINK)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(choice(config.DB_PHRASES), reply_markup=keyboard_markup)


def main_menu_indicators_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton(GET_CURR_NPS_DETAILING_BUTTON, callback_data=GET_CURR_NPS_DETAILING_BUTTON)],
        [InlineKeyboardButton(GET_SEMESTERS_DETAILING_BUTTON, callback_data=GET_SEMESTERS_DETAILING_BUTTON)],
        [InlineKeyboardButton(GET_GRADE_INFO_BUTTON, callback_data=GET_GRADE_INFO_BUTTON)]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Дополнительная информация", reply_markup=keyboard_markup)


def get_indicators_action(update: Update, context: CallbackContext) -> None:
    message = update.message.reply_text("Секундочку, чичас поищу")

    prep_id = update.effective_user.id
    values = get_values_from_sheet()

    nps, retirement, average_nps, average_retirement = get_prep_indicators(values, prep_id)

    if not nps and not retirement:
        message.edit_text("Ой, не могу найти ваши показатели 👉🏻👈🏻\n\n"
                          "Если вы преподаёте первый семестр, то просто дождитесь появления показателей.\n\n"
                          "В противном случае для добавления показателей в базу обратитесь к @ktrntrsv.")
    else:
        if nps and retirement:
            nps_evaluation = evaluation_indicator(nps=nps)
            retirement_evaluation = evaluation_indicator(retirement=retirement)

            message.edit_text(f"*Ваш NPS — {nps}*.\n"
                              f"Средний NPS по школе — {average_nps}.\n"
                              f"💭 `{nps_evaluation}`\n\n"
                              f"*Ваша выбываемость — {retirement}*.\n"
                              f"Средняя выбываемость по школе — {average_retirement}.\n"
                              f"💭 `{retirement_evaluation}`", parse_mode=ParseMode.MARKDOWN)

        elif nps and not retirement:
            message.edit_text(f"*Ваш NPS — {nps}*.\n"
                              f"Средний NPS по школе — {average_nps}.\n"
                              f"💭 `{evaluation_indicator(nps=nps)}`\n\n"
                              "Информации по вашей выбываемости я не нашёл 🧐 \n"
                              "Если вы думаете, что это ошибка, пожалуйста, обратитесь к @ktrntrsv ",
                              parse_mode=ParseMode.MARKDOWN)

        elif retirement and not nps:
            message.edit_text(f"*Ваша выбываемость — {retirement}*.\n"
                              f"Средняя выбываемость по школе — {average_retirement}.\n"
                              f"💭 `{evaluation_indicator(retirement=retirement)}\n\n"
                              "Информации по вашему NPS я не нашёл 🧐\n"
                              "Если вы думаете, что это ошибка, пожалуйста, обратитесь к @ktrntrsv",
                              parse_mode=ParseMode.MARKDOWN)

        keyboard = [
            [InlineKeyboardButton(GET_CURR_NPS_DETAILING_BUTTON, callback_data=GET_CURR_NPS_DETAILING_BUTTON)],
            [InlineKeyboardButton(GET_SEMESTERS_DETAILING_BUTTON, callback_data=GET_SEMESTERS_DETAILING_BUTTON)],
            [InlineKeyboardButton(GET_GRADE_INFO_BUTTON, callback_data=GET_GRADE_INFO_BUTTON)]
        ]
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Дополнительная информация", reply_markup=keyboard_markup)


def get_curr_nps_detailing_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Понятно", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]

    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("1. Детализация по группам\n2. Как считается мой NPS?", reply_markup=keyboard_markup)


def get_semester_detailing_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Предыдущий", callback_data=None),  # todo: fill callback
         InlineKeyboardButton("Следующий", callback_data=None)  # todo: fill callback
         ],

        [
            InlineKeyboardButton("Всё ясно", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("У вас отличная статистика. Чтобы узнать больше, пришлите смс на телефон 150-64-32.",
                            reply_markup=keyboard_markup)


def get_grade_info_action(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Принято", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    query.edit_message_text("*Вот так формируется грейд:*\n"
                            "Берется ваш NPS, смешивается с двумя стаканами слез девственицы, "
                            "делится на квадратный корень из двух умноженный на выбываемость и готово. \n\n"
                            "Но это только на растущую луну. При убывающей до сих пор никто понять не может",
                            parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_markup)


def undefined_message_button(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Не уверен, что понятийно 🥺\nЯ ещё не очень хорошо говорить русски, я молодой бот")


def init_dispatcher(updater: Update):
    logger.debug('Ининциализация диспетчера запросов')
    dispatcher = updater.dispatcher

    logger.debug('Добавление команды /start')
    dispatcher.add_handler(CommandHandler("start", start_command))

    logger.debug('Добавление обработки кнопок')
    dispatcher.add_handler(
        MessageHandler(Filters.regex('^' + GET_INDICATORS_BUTTON + '$'), get_indicators_action))

    dispatcher.add_handler(
        MessageHandler(Filters.regex('^' + GET_KD_LINK_BUTTON + '$'), get_kd_link_action))

    dispatcher.add_handler(
        CallbackQueryHandler(main_menu_indicators_action, pattern=GET_MAIN_MENU_INDICATORS))

    dispatcher.add_handler(
        CallbackQueryHandler(get_curr_nps_detailing_action, pattern=GET_CURR_NPS_DETAILING_BUTTON))

    dispatcher.add_handler(
        CallbackQueryHandler(get_semester_detailing_action, pattern=GET_SEMESTERS_DETAILING_BUTTON))

    dispatcher.add_handler(
        CallbackQueryHandler(get_grade_info_action, pattern=GET_GRADE_INFO_BUTTON))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_button))

    logger.info('Диспетчер запросов успешно инициализирован')
