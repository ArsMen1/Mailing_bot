from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.ext import CallbackContext
from loguru import logger

import mailing_bot.shp_mailing_bot.message_creator as messenger
from mailing_bot.shp_mailing_bot.config import GET_MAIN_MENU_INDICATORS
from mailing_bot.shp_mailing_bot.prep import Prep

logger.add('debug.log', encoding='utf8', rotation='10 MB', compression='zip')


def get_group_detailing_nps_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    try:
        query.answer()
    except error.BadRequest as ex:
        logger.critical(ex.message)
        # todo: обработать эту ситуацию как-нибудь
        return

    prep = Prep.find_prep(update)

    keyboard = [
        [
            InlineKeyboardButton(messenger.ok_message(), callback_data=GET_MAIN_MENU_INDICATORS)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(messenger.current_group_detailing_nps_message(prep.get_group_detailing()),
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.MARKDOWN)
