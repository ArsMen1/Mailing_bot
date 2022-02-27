from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import KNOWLEDGE_BASE_LINK
from mailing_bot.shp_mailing_bot.message_creator import kd_link_message
from mailing_bot.shp_mailing_bot.prep import Prep
from mailing_bot.logger_bot import logger
import mailing_bot.shp_mailing_bot.message_creator as messenger


def get_kd_link_action(update: Update, context: CallbackContext) -> None:  # get knowledge base link button


    keyboard = [
        [
            InlineKeyboardButton('База Знаний', url=KNOWLEDGE_BASE_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info(f"[{update.effective_user.name}] got Saint Knowledge Base link.")
    update.message.reply_text(kd_link_message(),
                              reply_markup=reply_markup)
