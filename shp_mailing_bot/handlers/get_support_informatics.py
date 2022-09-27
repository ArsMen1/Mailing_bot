from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from logger_bot import logger

from telegram.ext import CallbackContext


def get_support_informatics(update: Update, context: CallbackContext):
    logger.info(f"[{update.effective_user.name}] got support informatics link")
    keyboard = [
        [
            InlineKeyboardButton('Регламент техподдержки Информатикс', url="https://readymag.com/u359345956/3381839/")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f"@supinformatics — сюда вы можете обратиться, если у вас возникла проблема с Информатикс."
        f"\nПоддержка работает 5/2 с 9:30 до 18:00 ☘",
                              reply_markup=reply_markup)
