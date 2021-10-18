import time
from datetime import datetime

from loguru import logger
from telegram import InlineKeyboardMarkup, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, Filters

from shp_mailing_bot.config import CNC_SPREADSHEET_CELLS_RANGE, INITIAL_GREETING_MESSAGE, CNC_SPREADSHEET_ID, \
    SUPER_ADMINS
from shp_mailing_bot.google_auth import authorize

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
    :todo: Определить, зачем эта функция подключена в качестве handler'а
    """
    logger.debug('Запущена команда /check_access')
    try:
        chat_member = context.bot.getChatMember(-589285277, update.message.chat_id)
        print(f"{chat_member=}")
        return chat_member.status in ['administrator', 'creator', 'member']
    except BadRequest:

        return False


def send_nps(context) -> None:
    job = context.job
    context_data = job.context
    nps = read_nps(context.bot_data['sheet_data'], context_data)
    context.bot.send_message(context_data, text=nps)


def send_messages(context) -> None:
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


def start_command(update, context) -> None:
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


def start2(update):
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
    Организация рассылки по списку сообщений
    """

    text = update.message.text
    context.user_data['col_range'] = text
    data = get_group_sheet(context.user_data)
    message = context.bot.send_message(update.effective_chat.id, text='Начинаю отправлять сообщения...')
    send_messages_amount = 0
    who_message_was_not_sent_to = []
    chat_id_ind = data[0].index('chat id')
    user_name_ind = data[0].index('user')
    begin_ind, end_ind = tuple(map(int, context.user_data['col_range'].split(' ')))

    for row in data:
        if len(row) > chat_id_ind and row[chat_id_ind].isdigit():
            text = ' '.join(row[begin_ind:end_ind + 1])
            logger.info(row[begin_ind:end_ind + 1])
            logger.info(text)
            time.sleep(0.1)
            try:
                context.bot.send_message(row[chat_id_ind], text=text, parse_mode=ParseMode.MARKDOWN)
                send_messages_amount += 1
                message.edit_text(f'Отправляю сообщения... Уже отправил: {send_messages_amount}')
            except BadRequest as ex:
                who_message_was_not_sent_to.append(row[user_name_ind])
                logger.error(f'Ошибка отправки сообщения. Детали: {ex}. Пользователь {row[user_name_ind]}')
                # todo: доработать другую обработку разных исключений
            except Exception as ex:
                who_message_was_not_sent_to.append(row[user_name_ind])
                logger.error(f'Ошибка отправки сообщения. Детали: {ex}. Пользователь {row[user_name_ind]}')

    logger.info(f'Отправка завершена. Отправлено сообщений: {send_messages_amount}')
    logger.info(f'Не отправлено {who_message_was_not_sent_to}')

    if who_message_was_not_sent_to:
        message.edit_text(f'Отправка завершена. \n\nОтправлено сообщений: {send_messages_amount}' + ".\n" +
                          f'Не отправлено сообщений: {len(who_message_was_not_sent_to)}\n' +
                          'Кому не было отправлено:\n' + ",\n".join(who_message_was_not_sent_to) + "." + "\n👉🏻👈🏻")
    else:
        message.edit_text(f'Отправка завершена. \n\nОтправлено сообщений: {send_messages_amount}. \n' +
                          f'Все сообщения были отправлены 😎')

    # superadmins mailing
    for admin_name, admin_id in SUPER_ADMINS.items():
        context.bot.send_message(admin_id,
                                 text="*Уведомление о рассылке*📨\n\n" +
                                      f"*Отправитель*: @{update.message.from_user.username}\n\n" +
                                      f"*Сообщение:* \n{text}",
                                 parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END


def back_to_menu(update, context):
    context.user_data.clear()
    start2(update)


def stop_conversation(update):
    update.message.reply_text("Пока-пока")
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
