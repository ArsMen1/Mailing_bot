from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import mailing_bot.shp_mailing_bot.message_creator as messenger
from mailing_bot.shp_mailing_bot.config import GET_MAIN_MENU_INDICATORS


def get_group_detailing_nps_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(messenger.ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(messenger.current_group_detailing_nps_message(), reply_markup=reply_markup)
