from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext


def get_contact(update: Update, context: CallbackContext):
    target_chat_username = 'invain_n'  # Замените на username чата, в который вы хотите перейти

    keyboard = [[InlineKeyboardButton("Перейти", url=f"https://t.me/{target_chat_username}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Чат с сотрудником ВУЦ", reply_markup=reply_markup)
