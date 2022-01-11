from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import GET_GRADE_INFO_BUTTON, GET_GROUP_DETAILING_NPS_BUTTON, \
    GET_SEMESTERS_DETAILING_BUTTON
import mailing_bot.shp_mailing_bot.message_creator as messenger
from mailing_bot.shp_mailing_bot.indicators_processing import get_prep_indicators
from mailing_bot.shp_mailing_bot.google_sheets_info import get_indicators_from_sheet


def get_indicators_action(update: Update, context: CallbackContext) -> None:
    message = update.message.reply_text('Секундочку, чичас поищу')

    prep_id = update.effective_user.id
    values = get_indicators_from_sheet()

    nps, retirement, average_nps, average_retirement, redflags = get_prep_indicators(values, prep_id)

    final_indicators_message, indicators_flag = messenger.indicators_message(nps,
                                                                             retirement,
                                                                             average_nps,
                                                                             average_retirement,
                                                                             redflags)

    if not indicators_flag:  # if no indicators information

        keyboard = [
            [InlineKeyboardButton('Формирование грейда', callback_data=GET_GRADE_INFO_BUTTON)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message.edit_text(final_indicators_message, parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text('Дополнительная информация', reply_markup=reply_markup)
        return
    else:
        keyboard = [
            [InlineKeyboardButton('Мой NPS по группам', callback_data=GET_GROUP_DETAILING_NPS_BUTTON)],
            [InlineKeyboardButton('Мой NPS по семестрам', callback_data=GET_SEMESTERS_DETAILING_BUTTON)],
            [InlineKeyboardButton('Формирование грейда', callback_data=GET_GRADE_INFO_BUTTON)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message.edit_text(final_indicators_message, parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text('Дополнительная информация', reply_markup=reply_markup)
