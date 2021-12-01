import mailing_bot.shp_mailing_bot.config as config
from random import choice
from time import sleep

from loguru import logger

from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler, Handler

from mailing_bot.shp_mailing_bot.google_sheets_info import get_values_from_sheet

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')

GET_KD_LINK_BUTTON = "База знаний"

GET_INDICATORS_BUTTON = "Мои показатели"

GET_MAIN_MENU_INDICATORS = "Главное меню"
GET_CURR_NPS_DETAILING_BUTTON = "NPS по группам"
GET_SEMESTERS_DETAILING_BUTTON = "NPS по семестрам"
GET_GRADE_INFO_BUTTON = "Грейд"

GET_NEXT_SEM_NPS = "Следующий"
GET_PREV_SEM_NPS = "Предыдущий"


def get_prep_indicators(values: list, prep_id: int) -> tuple:  # table info parser
    # getting average info
    average_nps = values[0][2]
    average_retirement = values[0][3]

    nps = 0
    retirement = 0
    redflags = 0

    # getting prep info
    for prep_info in values:
        if prep_info[1].isdigit() and int(prep_info[1]) == prep_id:
            logger.debug(prep_info)
            if len(prep_info) >= 3:  # if nps and no retirement and no redflags
                nps = prep_info[2]
            if len(prep_info) >= 4:  # if nps and retirement and no redflags
                retirement = prep_info[3]
            if len(prep_info) >= 5:  # if nps and retirement and redflags
                redflags = prep_info[4]
    return nps, retirement, average_nps, average_retirement, redflags


def evaluation_indicator(nps: str = None, retirement: str = None) -> str:  # get comment for nps or retirement
    if nps and nps[-1] == "%":
        nps = float(nps.replace(",", ".")[:-1])
    if retirement and retirement[-1] == "%":
        retirement = retirement.replace(",", ".")[:-1]

    if (nps and nps >= config.TOP_BAR_NPS) or \
            (retirement and float(retirement) <= config.TOP_BAR_RETIREMENT):
        return choice(config.EXCELLENT_INDICATORS_COMMENTS)

    elif (nps and config.MEDIUM_BAR_NPS <= nps < config.TOP_BAR_NPS) or \
            (retirement and config.MEDIUM_BAR_RETIREMENT >= float(retirement) >= config.TOP_BAR_RETIREMENT):
        return choice(config.GOOD_INDICATORS_COMMENTS)

    elif (nps and nps < config.MEDIUM_BAR_NPS) or \
            (retirement and float(retirement) > config.MEDIUM_BAR_RETIREMENT):
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

    nps, retirement, average_nps, average_retirement, redflags = get_prep_indicators(values, prep_id)

    redflags_message = ""
    if redflags:
        redflags_message = f"\n\n*Количество редфлагов — {redflags}.*\n" \
                           f"Для уточнения информации по причинам получения рефдлагов обратитесь к вашему руководителю."

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
                              f"💭 `{retirement_evaluation}`" + redflags_message, parse_mode=ParseMode.MARKDOWN)

        elif nps and not retirement:
            message.edit_text(f"*Ваш NPS — {nps}*.\n"
                              f"Средний NPS по школе — {average_nps}.\n"
                              f"💭 `{evaluation_indicator(nps=nps)}`\n\n"
                              "Информации по вашей выбываемости я не нашёл 🧐 \n"
                              "Если вы думаете, что это ошибка, пожалуйста, обратитесь к @ktrntrsv " + redflags_message,
                              parse_mode=ParseMode.MARKDOWN)

        elif retirement and not nps:
            message.edit_text(f"*Ваша выбываемость — {retirement}*.\n"
                              f"Средняя выбываемость по школе — {average_retirement}.\n"
                              f"💭 `{evaluation_indicator(retirement=retirement)}\n\n"
                              "Информации по вашему NPS я не нашёл 🧐\n"
                              "Если вы думаете, что это ошибка, пожалуйста, обратитесь к @ktrntrsv" + redflags_message,
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


def get_next_semester_stat_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM_NPS),
         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM_NPS)
         ],

        [
            InlineKeyboardButton("Всё ясно", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Статистика следующего семестра",
                            reply_markup=keyboard_markup)


def get_prev_semester_stat_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM_NPS),
         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM_NPS)
         ],

        [
            InlineKeyboardButton("Всё ясно", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Статистика предыдущего семестра",
                            reply_markup=keyboard_markup)


def get_semester_detailing_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM_NPS),
         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM_NPS)
         ],

        [
            InlineKeyboardButton("Всё ясно", callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("У вас отличная статистика. Чтобы узнать больше, пришлите смс на телефон 150-64-32.",
                            reply_markup=keyboard_markup)


def get_grade_info_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Как формируется NPS?", callback_data=GET_MAIN_MENU_INDICATORS)],  # todo: change callback
        [InlineKeyboardButton("А выбываемость?", callback_data=GET_MAIN_MENU_INDICATORS)],  # todo: change callback
        [InlineKeyboardButton("Что за редфлаги?", callback_data=GET_MAIN_MENU_INDICATORS)],  # todo: change callback
        [InlineKeyboardButton("Всё ясно, давай обратно", callback_data=GET_MAIN_MENU_INDICATORS)]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    n = " " * 8
    query.edit_message_text("*Грейд 3:*\n" +
                            n + "NPS >=83%\n" +
                            n + "Выбываемость <= 7%\n" +
                            n + "🤑 Премия — 30%\n\n"
                                       "*Грейд 2:*\n" +
                            n + "NPS >= 72%\n" +
                            n + "Выбываемость <= 10%\n" +
                            n + "💰 Премия — 15%\n\n"
                                       "*Грейд 1:*\n" +
                            n + "NPS  >= 60%\n" +
                            n + "Выбываемость <= 13%\n" +
                            n + "💵 Премия — 5%\n\n"
                                       "*Грейд 0:*\n" +
                            n + "NPS  < 60%\n" +
                            n + "Выбываемость > 13%\n" +
                            n + "💸 Премия — 0%\n\n"
                                       "*Итоговый грейд — минимальный из двух грейдов по NPS и по выбываемости*.\n\n"
                            "Редфлаги тоже влияют на премию, но я пока не поняла, как. Попозже зайди",
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
        CallbackQueryHandler(get_next_semester_stat_action, pattern=GET_NEXT_SEM_NPS))

    dispatcher.add_handler(
        CallbackQueryHandler(get_prev_semester_stat_action, pattern=GET_PREV_SEM_NPS))

    dispatcher.add_handler(
        CallbackQueryHandler(get_grade_info_action, pattern=GET_GRADE_INFO_BUTTON))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_button))

    logger.info('Диспетчер запросов успешно инициализирован')
