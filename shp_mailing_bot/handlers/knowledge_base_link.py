from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import KNOWLEDGE_BASE_LINK
from mailing_bot.shp_mailing_bot.message_creator import kd_link_message
from mailing_bot.shp_mailing_bot.prep import Prep
import mailing_bot.shp_mailing_bot.message_creator as messenger


def get_kd_link_action(update: Update, context: CallbackContext) -> None:  # get knowledge base link button
    prep_id = update.effective_user.id

    if prep_id not in Prep.preps_cashed_list:
        prep = Prep(prep_id)
        if not prep.does_exists:
            update.message.reply_text(messenger.are_you_really_prep)
            return
        Prep.preps_cashed_list[prep_id] = prep
    keyboard = [
        [
            InlineKeyboardButton('База Знаний', url=KNOWLEDGE_BASE_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(kd_link_message(),
                              reply_markup=reply_markup)
