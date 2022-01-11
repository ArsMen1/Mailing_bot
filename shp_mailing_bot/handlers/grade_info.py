from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import GRADE_ARTICLE_KB, GET_MAIN_MENU_INDICATORS
import mailing_bot.shp_mailing_bot.message_creator as messenger


def get_grade_info_action(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton('Статья в Базе Знаний', url=GRADE_ARTICLE_KB)],
        [InlineKeyboardButton(messenger.ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(messenger.grade_info_message(),
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
