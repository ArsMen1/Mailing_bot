from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import GET_GROUP_DETAILING_NPS_BUTTON, GET_SEMESTERS_DETAILING_BUTTON, \
    GET_GRADE_INFO_BUTTON


def main_menu_indicators_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton('Мой NPS по группам', callback_data=GET_GROUP_DETAILING_NPS_BUTTON)],
        [InlineKeyboardButton('Мой NPS по семестрам', callback_data=GET_SEMESTERS_DETAILING_BUTTON)],
        [InlineKeyboardButton('Формирование грейда', callback_data=GET_GRADE_INFO_BUTTON)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text('Дополнительная информация', reply_markup=reply_markup)
