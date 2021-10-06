import os
from os.path import join, dirname
import time
from loguru import logger
from datetime import datetime
from google_oath import authorizate
from telegram.error import BadRequest
from telegram import InlineKeyboardMarkup, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, Filters

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# The ID and range of a sample spreadsheet.
MAIN_SPREADSHEET_ID = os.getenv('READ_SPREADSHEET2')
BOT_TOKEN = os.getenv('BOT_TOKEN_TEST')
RANGE_NAME = 'Data!A1:А13'

logger.add(
    'debug.log',
    encoding="utf8",
    format='TIME: {time} LEVEL: {level} MESSAGE: {message}',
    rotation='10 MB',
    compression='zip'
)

IND_MAILING, SHEET_ID, LIST_NAME, COL_RANGE, INTERRUPT = range(5)

interrupt_keyboard = [['Завершить разговор']]
interrupt_markup = ReplyKeyboardMarkup(interrupt_keyboard, resize_keyboard=True, one_time_keyboard=True)


def read_data(sheets_service):
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=MAIN_SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def read_nps(sheet_data, chat_id):
    print(sheet_data, chat_id)
    nps = None
    for row in sheet_data:
        if row[0] == str(chat_id):
            nps = row[9]
    if not nps:
        return 'NPS not found'
    return nps


def check_access(update, context):
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
    message = context.bot.send_message(query.from_user.id, text='Рассылка завершена')


def button(update, context) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    if query.data == 'NPS':
        context.job_queue.run_once(send_nps, 0, context=query.from_user.id)
    if query.data == 'send messages':
        context.job_queue.run_once(send_messages, 0, context=query)


def start_command(update, context):
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
            '\n\n'.join([
                '👋🏻 Привет, преподаватель Школы программистов!'
                '*Этот бот был разработан, чтобы оперативно доставлять всю важную информацию лично тебе!*'
                'Совсем скоро сюда начнут приходить первые сообщения – не пропусти их 😉'
            ]),
            reply_markup=reply_markup_user,
            parse_mode=ParseMode.MARKDOWN
        )


def get_group_sheet(user_data):
    service = authorizate()
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
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    file_name = f'Рассылка {dt_string}.txt'
    f = open(file_name, "w")
    text = update.message.text
    context.user_data['col_range'] = text
    data = get_group_sheet(context.user_data)
    message = context.bot.send_message(update.effective_chat.id, text='Начинаю отправлять сообщения...')
    send = 0
    not_send = 0
    chat_id_ind = data[0].index('chat id')
    user_name_ind = data[0].index('user')
    begin_ind, end_ind = tuple(map(int, context.user_data['col_range'].split(' ')))
    for row in data:
        if len(row) > chat_id_ind and row[chat_id_ind].isdigit():
            text = ' '.join(row[begin_ind:end_ind + 1])
            try:
                context.bot.send_message(row[chat_id_ind], text=text, parse_mode=ParseMode.MARKDOWN)
                send += 1
                message.edit_text(f'Отправляю сообщения... Уже отправил: {send}')
            except:
                f.write(row[user_name_ind])
                f.write(' — ')
                f.write(row[chat_id_ind])
                f.write('\n')
                not_send += 1
            time.sleep(0.1)
    message.edit_text(f'Отправка завершена! Отправлено сообщений: {send}')
    update.message.reply_text(f'Не отправлено сообщений: {not_send}')
    f.close()
    return ConversationHandler.END


def back_to_menu(update, context):
    context.user_data.clear()
    start2(update, context)


def stop_conversation(update, context):
    update.message.reply_text("Bye!")
    return ConversationHandler.END


def init_telegram():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('check_access', check_access)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(CallbackQueryHandler(button))

    states = {
        IND_MAILING: [MessageHandler(Filters.regex('^Групповая рассылка$'), ind_mailing)],
        SHEET_ID: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_sheet_id)],
        LIST_NAME: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_list_name)],
        COL_RANGE: [MessageHandler(Filters.regex('^(?!Завершить разговор).*$'), add_col_range)],
    }
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start2', start2)],
        states=states,
        fallbacks=[
            MessageHandler(Filters.regex('^Завершить разговор$'), stop_conversation)
        ]
    )
    dispatcher.add_handler(conv_handler)

    logger.info('Bot start polling')
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    init_telegram()
