from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from loguru import logger

from mailing_bot.shp_mailing_bot.config import GET_GRADE_INFO_BUTTON, GET_GROUP_DETAILING_NPS_BUTTON, \
    GET_SEMESTERS_DETAILING_BUTTON
import mailing_bot.shp_mailing_bot.message_creator as messenger
from mailing_bot.shp_mailing_bot.prep import Prep

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')


def get_indicators_action(update: Update, context: CallbackContext) -> None:
    message = update.message.reply_text('Секундочку, чичас поищу')
    prep_id = update.effective_user.id
    if prep_id not in Prep.preps_cashed_list:
        Prep.preps_cashed_list[prep_id] = Prep(prep_id)
    prep = Prep.preps_cashed_list[prep_id]
    nps, retirement, redflags, average_nps, average_retirement = (None,) * 5

    nps, retirement, redflags = prep.get_curr_nps(), prep.get_curr_retirement(), prep.get_curr_redflags()

    if any((nps, retirement, redflags)):
        average_nps, average_retirement = prep.average_curr_nps, prep.average_curr_retirement

    final_indicators_message, indicators_flag = messenger.indicators_message(nps,
                                                                             retirement,
                                                                             average_nps,
                                                                             average_retirement,
                                                                             redflags)

    # keyboard generating
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
