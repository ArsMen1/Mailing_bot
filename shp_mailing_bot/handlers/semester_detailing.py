from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.message_creator import ok_message
from mailing_bot.shp_mailing_bot.config import GET_MAIN_MENU_INDICATORS
from mailing_bot.shp_mailing_bot.notion_api import get_sem_indicators

I_18_19_SEM = "1 семестр 18-19"
II_18_19_SEM = "2 семестр 18-19"
I_19_20_SEM = "1 семестр 19-20"
II_19_20_SEM = "2 семестр 19-20"
I_20_21_SEM = "1 семестр 20-21"
II_20_21_SEM = "2 семестр 20-21"
I_21_22_SEM = "1 семестр 21-22"
II_21_22_SEM = "2 семестр 21-22"


def i_18_19_sem_nps(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton('Предыдущий', callback_data=GET_PREV_SEM_NPS),
         InlineKeyboardButton('Следующий', callback_data=GET_NEXT_SEM_NPS)
         ],

        [
            InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('', reply_markup=keyboard_markup)


def ii_18_19_sem_nps(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton('Предыдущий', callback_data=GET_PREV_SEM_NPS),
            InlineKeyboardButton('Следующий', callback_data=GET_NEXT_SEM_NPS)
        ],

        [
            InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('', reply_markup=keyboard_markup)


def i_19_20_sem_nps(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton('Предыдущий', callback_data=GET_PREV_SEM_NPS),
         InlineKeyboardButton('Следующий', callback_data=GET_NEXT_SEM_NPS)
         ],

        [
            InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text('', reply_markup=reply_markup)


def ii_19_20_sem_nps(update: Update, context: CallbackContext):
    pass


def i_20_21_sem_nps(update: Update, context: CallbackContext):
    pass


def ii_20_21_sem_nps(update: Update, context: CallbackContext):
    pass


def i_21_22_sem_nps(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if is_there_last_sem and is_there_next_sem:
        keyboard = [
            [InlineKeyboardButton('Предыдущий', callback_data=GET_PREV_SEM_NPS),
             InlineKeyboardButton('Следующий', callback_data=GET_NEXT_SEM_NPS)
             ],

            [
                InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    elif is_there_last_sem:
        keyboard = [
            [InlineKeyboardButton('Предыдущий', callback_data=GET_PREV_SEM_NPS),
             ],

            [
                InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    elif is_there_next_sem:
        pass
    else:
        keyboard = [[InlineKeyboardButton(ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)]]
        reply_markup = InlineKeyboardMarkup(keyboard)


    query.edit_message_text('', reply_markup=reply_markup)


def ii_21_22_sem_nps(update: Update, context: CallbackContext):
    pass
