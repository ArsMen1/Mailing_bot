import os
import sys
import time
from loguru import logger
from datetime import datetime

from telegram.error import BadRequest, InvalidToken
from telegram import InlineKeyboardMarkup, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, Filters

from dotenv import load_dotenv

from shp_mailing_bot.config import CNC_SPREADSHEET_CELLS_RANGE, INITIAL_GREETING_MESSAGE
from shp_mailing_bot.google_auth import authorize

load_dotenv()
CNC_SPREADSHEET_ID = os.getenv('CNC_SPREADSHEET_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logger.add(
    'debug.log',
    encoding="utf8",
    format='TIME: {time:DD-MM-YYYY at HH:mm:ss} LEVEL: {level} MESSAGE: {message}',
    rotation='10 MB',
    compression='zip'
)

IND_MAILING, SHEET_ID, LIST_NAME, COL_RANGE, INTERRUPT = range(5)

interrupt_keyboard = [['Завершить разговор']]
interrupt_markup = ReplyKeyboardMarkup(interrupt_keyboard, resize_keyboard=True, one_time_keyboard=True)


def read_data(sheets_service):
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=CNC_SPREADSHEET_ID, range=CNC_SPREADSHEET_CELLS_RANGE).execute()
    values = result.get('values', [])
    return values


def read_nps(sheet_data, chat_id):
    nps = None
    for row in sheet_data:
        if row[0] == str(chat_id):
            nps = row[9]
    if not nps:
        return 'NPS not found'
    return nps


def check_access(update, context) -> bool:
    """
    Проверка прав доступа у пользователя, запускающего команду рассылки

    Если пользователь присутствует в чате и имеет роль админа/создателя/участника - возвращается True. Иначе False

    :param update: событие обновления
    :param context: контекст события
    """
    try:
        chat_member = context.bot.getChatMember(-589285277, update.message.chat_id)
        return chat_member.status in ['administrator', 'creator', 'member']
    except BadRequest:
        return False


def send_nps(context):
    job = context.job
    context_data = job.context
    nps = read_nps(context.bot_data['sheet_data'], context_data)
    context.bot.send_message(context_data, text=nps)


def send_messages(context):
    job = context.job
    query = job.context
    message = context.bot.send_message(query.from_user.id, text='Начинаю отправлять сообщения')
    i = 0
    for row in context.bot_data['sheet_data']:
        if row[0]:
            context.bot.send_message(int(row[0]), text=row[9])
            i += 1
            message.edit_text(f'Отправил сообщений: {i}')
            time.sleep(0.1)
    context.bot.send_message(query.from_user.id, text='Рассылка завершена')


def button(update, context) -> None:
    """
    [Предположительно] Обработчик нажатия кнопки на виртуальной клавиатуре (там, где две кнопки).
    """
    query = update.callback_query
    query.answer()
    if query.data == 'NPS':
        context.job_queue.run_once(send_nps, 0, context=query.from_user.id)
    if query.data == 'send messages':
        context.job_queue.run_once(send_messages, 0, context=query)


def start_command(update, context):
    """
    Обработчик команды `/start`
    """
    is_admin = check_access(update, context)
    keyboard_user = [
        [
        ]
    ]

    keyboard_admin2 = [[KeyboardButton('text')]]
    reply_markup_user = InlineKeyboardMarkup(keyboard_user)
    reply_markup_admin = ReplyKeyboardMarkup(keyboard=keyboard_admin2, resize_keyboard=True, one_time_keyboard=True)

    if is_admin:
        update.message.reply_text('Выберите команду', reply_markup=reply_markup_admin)
    else:
        update.message.reply_text(
            INITIAL_GREETING_MESSAGE,
            reply_markup=reply_markup_user,
            parse_mode=ParseMode.MARKDOWN
        )


def get_group_sheet(user_data):
    service = authorize()
    sheet = service.spreadsheets()
    lst = user_data['list_id']
    result = sheet.values().get(spreadsheetId=user_data['sheet_id'], range=f'{lst}!A1:K1000').execute()
    values = result.get('values', [])
    return values


def start2(update, context):
    keyboard = [
        ['Индивидуальная рассылка'],
        ['Групповая рассылка']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Выберите команду', reply_markup=reply_markup)
    return IND_MAILING


def ind_mailing(update, context):
    text = update.message.text
    context.user_data['choise'] = text
    update.message.reply_text('Отправьте id гугл-таблицы', reply_markup=interrupt_markup)
    return SHEET_ID


def add_sheet_id(update, context):
    text = update.message.text
    context.user_data['sheet_id'] = text
    update.message.reply_text('Отправьте точное название листа', reply_markup=interrupt_markup)
    return LIST_NAME


def add_list_name(update, context):
    text = update.message.text
    context.user_data['list_id'] = text
    update.message.reply_text('Отправьте через пробел номера первого и последнего ', reply_markup=interrupt_markup)
    return COL_RANGE


def add_col_range(update, context):
    """
    [Предположительно] Организация рассылки по списку сообщений
    """
    status_file_name = f'Рассылка {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}.txt'
    status_file = open(status_file_name, "w")
    text = update.message.text
    context.user_data['col_range'] = text
    data = get_group_sheet(context.user_data)
    message = context.bot.send_message(update.effective_chat.id, text='Начинаю отправлять сообщения...')
    send_messages_amount = 0
    not_send_messages_amount = 0
    chat_id_ind = data[0].index('chat id')
    user_name_ind = data[0].index('user')
    begin_ind, end_ind = tuple(map(int, context.user_data['col_range'].split(' ')))
    for row in data:
        if len(row) > chat_id_ind and row[chat_id_ind].isdigit():
            text = ' '.join(row[begin_ind:end_ind + 1])
            try:
                context.bot.send_message(row[chat_id_ind], text=text, parse_mode=ParseMode.MARKDOWN)
                send_messages_amount += 1
                message.edit_text(f'Отправляю сообщения... Уже отправил: {send_messages_amount}')
            except Exception as ex:
                status_file.write(f'{row[user_name_ind]} - {row[chat_id_ind]}\n')
                not_send_messages_amount += 1
                logger.error(f'Ошибка отправки сообщения. Детали: {ex}')
            time.sleep(0.1)
    message.edit_text(f'Отправка завершена! Отправлено сообщений: {send_messages_amount}')
    logger.info(f'Отправка завершена! Отправлено сообщений: {send_messages_amount}')
    update.message.reply_text(f'Не отправлено сообщений: {not_send_messages_amount}')
    status_file.close()
    return ConversationHandler.END


def back_to_menu(update, context):
    context.user_data.clear()
    start2(update, context)


def stop_conversation(update, context):
    update.message.reply_text("Bye!")
    return ConversationHandler.END


def init_dispatcher(updater):
    """
    Задание структуры бота (тех команд, на которые он будет способен реагировать)
    """
    logger.debug('Ининциализация диспетчера запросов')
    dispatcher = updater.dispatcher

    logger.debug('Добавление команды /start')
    dispatcher.add_handler(CommandHandler('start', start_command))

    logger.debug('Добавление команды /check_access')
    dispatcher.add_handler(CommandHandler('check_access', check_access))

    logger.debug('Добавление обработки кнопок')
    dispatcher.add_handler(CallbackQueryHandler(button))

    logger.debug('Добавление команды /start2')
    states = {
        IND_MAILING: [MessageHandler(Filters.regex('^Групповая рассылка$'), ind_mailing)],
        SHEET_ID: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_sheet_id)],
        LIST_NAME: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_list_name)],
        COL_RANGE: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_col_range)],
    }
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start2', start2)
        ],
        states=states,
        fallbacks=[
            MessageHandler(Filters.regex('^Завершить разговор$'), stop_conversation)
        ]
    )
    dispatcher.add_handler(conv_handler)
    logger.info('Диспетчер запросов успешно инициализирован')


def init_telegram():
    try:
        logger.debug('Запуск')
        logger.debug('Подключение к telegram API...')
        updater = Updater(token=TELEGRAM_BOT_TOKEN)
        logger.info('Подключение к telegram API установлено.')
        init_dispatcher(updater)
        logger.info('Bot start polling')
        updater.start_polling()
        updater.idle()
    except InvalidToken as ex:
        logger.critical('В настройках бота указан некорректный токен. Дальнейшая работа бота невозможна, выключение.')
        sys.exit(1)
