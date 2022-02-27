from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot import message_creator as messenger
from mailing_bot.shp_mailing_bot.config import semesters_names, ACTUAL_SEM
from mailing_bot.shp_mailing_bot.handlers.get_prep_indicators_main import get_indicators, get_right_keyboard
from mailing_bot.shp_mailing_bot.prep import Prep
from mailing_bot.logger_bot import logger


def semesters_navigator(change_sem_func):
    def wrapper(update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        prep = Prep(update.effective_user.id, update.effective_user.name)

        change_sem_func(update, context, prep)

        sem = semesters_names[prep.sem_pointer]
        final_message = f"*Семестр {sem}\n\n\n*"

        if not get_indicators(prep):
            final_message += "Тут ничего нет и не было 😶‍🌫️"
        else:
            final_message = final_message + get_indicators(prep) + \
                            messenger.grade_info_message(prep.semesters_indicators[sem].grade,
                                                         actual_sem=(sem == ACTUAL_SEM)) + \
                            messenger.current_group_detailing_nps_message(
                                prep.semesters_indicators[sem].group_detailing)

        reply_markup = get_right_keyboard(prep)
        query.edit_message_text(final_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        logger.info(f"[{prep.prep_tg_name}] goes to {sem=}")

    return wrapper


@semesters_navigator
def get_prev_sem_indicators_action(update: Update, context: CallbackContext, prep) -> None:
    prep.sem_pointer -= 1


@semesters_navigator
def get_next_sem_indicators_action(update: Update, context: CallbackContext, prep):
    prep.sem_pointer += 1
