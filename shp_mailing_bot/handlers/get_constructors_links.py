from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from shp_mailing_bot.config import LESSON_CONSTRUCTOR_JA, LESSON_CONSTRUCTOR_MD, CONSTRUCTOR_SUGGESTIONS_FORM_LINK
from shp_mailing_bot.prep import Prep
from logger_bot import logger


def get_constructors_links(update: Update, context: CallbackContext) -> None:
    prep = Prep(update.effective_user.id, update.effective_user.name)
    if not prep.status:
        update.message.reply_text("Ой, здравствуйте, мы с вами разве знакомы?")
        return

    keyboard = [
        [InlineKeyboardButton('Конструктор урока – J/A', url=LESSON_CONSTRUCTOR_JA)],
        [InlineKeyboardButton('Конструктор урока – M/D', url=LESSON_CONSTRUCTOR_MD)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = "Если вы знаете хороший приём, который может быть включён в конструктор, " \
                   "пожалуйста, поделитесь с коллегами своей гениальностью и " \
                   f"заполните [эту форму]({CONSTRUCTOR_SUGGESTIONS_FORM_LINK}).\n\n" \
                   "Ваш приём будет добавлен в конструктор со ссылкой на вас.\n" \
                   "Прекрасная возможность войти в историю 😄"

    logger.info(f"[{update.effective_user.name}] got constructors links.")
    update.message.reply_text(message_text,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.MARKDOWN)
