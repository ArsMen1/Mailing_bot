from telegram import Update
from logger_bot import logger

from telegram.ext import CallbackContext

from shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT


def help_action(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Если вы столкнулись с проблемой, связанной со мной, '
        'чувствуете злость, негодование, обиду, презрение или просто растерянность, '
        'вдохните и выдохните на 10 счётов 🧘 \n\n'
        f'А потом напишите {RESPONSIBLE_FOR_THE_BOT}, она поможет разобраться с проблемой :)')
    logger.info(f"[{update.effective_user.name}] help message sent.")
