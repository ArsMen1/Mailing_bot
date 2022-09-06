from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from shp_mailing_bot.message_creator import get_personal_page_phrase


from shp_mailing_bot.prep import Prep
from logger_bot import logger


def get_personal_page_action(update: Update, context: CallbackContext) -> None:  # get knowledge base link button
    prep = Prep(update.effective_user.id, update.effective_user.name)
    if not prep.personal_page_link:
        update.message.reply_text("Ой, у вас нет личной странички 🫣\n\n"
                                  "Но вы можете её завести, для этого напишите любому сотруднику ВУЦ 🙃")
        logger.info(f"[{update.effective_user.name}] has no personal page.")
        return

    keyboard = [
        [
            InlineKeyboardButton('Моя страница', url=prep.personal_page_link)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info(f"[{update.effective_user.name}] got personal page.")
    update.message.reply_text(get_personal_page_phrase(),
                              reply_markup=reply_markup)
