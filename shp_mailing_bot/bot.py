from telegram import Update, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, \
    CallbackQueryHandler

import shp_mailing_bot.handlers.get_prep_indicators_semester_navigation
from logger_bot import logger
from shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT, GET_NEXT_SEM, GET_PREV_SEM
from shp_mailing_bot.message_creator import get_name_patronymic, are_you_really_prep_message

from shp_mailing_bot.handlers import get_prep_indicators_main, knowledge_base_link, get_support_ea_tg
from shp_mailing_bot.prep import Prep


def start_action(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    prep = Prep(update.effective_user.id, update.effective_user.name)
    if not prep.status:
        update.message.reply_text(are_you_really_prep_message)
        return
    update.message.reply_text(f'Здравствуйте, {get_name_patronymic(prep.name)}! '
                              f'Рад, что вы заглянули ко мне в гости :)\n\n'
                              f'*Я бот для преподавателей Школы Программистов.* '
                              f'Я очень полезный ☺️\n\n'
                              f'▫️Буду *присылать вам важную информацию*, '
                              f'которую мне передают мои секретные агенты. Только тсс 🤫\n'
                              f'▫️Также в моей книжечке записаны *ваши показатели* (NPS, выбываемость, грейд), '
                              f'которыми я могу поделиться с вами по секрету.\n'
                              f'▫ А ещё, если вы потеряете мою подругу *Базу Знаний*, я помогу ее найти.\n\n'
                              f'\nДавайте осмотримся, введите "/" или воспользуйтесь меню команд.',
                              parse_mode=ParseMode.MARKDOWN)
    # update.message.reply_text(f"Здравствуйте, {get_name_patronymic(prep.name)}.")
    logger.info(f'[{prep.prep_tg_name}] start message sent.')


def help_action(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Если вы столкнулись с проблемой, связанной со мной, '
        'чувствуете злость, негодование, обиду, презрение или просто растерянность, '
        'вдохните и выдохните на 10 счётов 🧘 \n\n'
        f'А потом напишите {RESPONSIBLE_FOR_THE_BOT}. \nЭто моя мамочка, она будет рада обратной связи.')
    logger.info(f"[{update.effective_user.name}] help message sent.")


def undefined_message_action(update: Update, context: CallbackContext):
    update.message.reply_text('Не уверен, что понятийно 🥺\n'
                              'Я ещё не очень хорошо говорить русски, я молодой бот. \n'
                              'Используйтэ команда с "/"')
    logger.info(f"[{update.effective_user.name}] wrote bullshit")


def init_dispatcher(updater: Update):
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_action))

    dispatcher.add_handler(CommandHandler('help', help_action))

    dispatcher.add_handler(CommandHandler('get_indicators', get_prep_indicators_main.get_indicators_action))

    dispatcher.add_handler(CallbackQueryHandler(
        shp_mailing_bot.handlers.get_prep_indicators_semester_navigation.get_prev_sem_indicators_action,
        pattern=GET_PREV_SEM))
    # get previous semester handler

    dispatcher.add_handler(CallbackQueryHandler(
        shp_mailing_bot.handlers.get_prep_indicators_semester_navigation.get_next_sem_indicators_action,
        pattern=GET_NEXT_SEM))
    # get next semester handler

    dispatcher.add_handler(CommandHandler('knowledge_base', knowledge_base_link.get_kd_link_action))

    dispatcher.add_handler(CommandHandler('get_support_eduApp', get_support_ea_tg.get_support_ea))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, undefined_message_action))

    logger.info('Dispatcher initialized successfully.')
