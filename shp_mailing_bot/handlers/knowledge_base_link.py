from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import KNOWLEDGE_BASE_LINK
from mailing_bot.shp_mailing_bot.message_creator import kd_link_message


def get_kd_link_action(update: Update, context: CallbackContext) -> None:  # get knowledge base link button
    keyboard = [
        [
            InlineKeyboardButton('База Знаний', url=KNOWLEDGE_BASE_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(kd_link_message(),
                              reply_markup=reply_markup)
