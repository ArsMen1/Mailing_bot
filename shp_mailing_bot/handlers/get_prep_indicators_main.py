from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from typing import Union

from mailing_bot.shp_mailing_bot.config import GET_PREV_SEM, GET_NEXT_SEM, ACTUAL_SEM
import mailing_bot.shp_mailing_bot.message_creator as messenger
from mailing_bot.shp_mailing_bot.prep import Prep, semesters_names
from mailing_bot.logger_bot import logger

prev_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий семестр", callback_data=GET_PREV_SEM)]
                                      ])
next_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Следующий семестр", callback_data=GET_NEXT_SEM)]
                                      ])
double_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM),
                                         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM)]
                                        ])


def get_indicators(prep: Prep) -> Union[str, None]:
    sem = semesters_names[prep.sem_pointer]
    indicators = prep.semesters_indicators[sem]

    actual_sem_flag = False

    if sem == ACTUAL_SEM:
        actual_sem_flag = True

    if indicators and any((indicators.nps,
                           indicators.retirement,
                           indicators.redflags)):
        average_nps, average_retirement = prep.average_indicators[sem]
        indicators_message, indicators_flag = messenger.indicators_message(indicators.nps,
                                                                           indicators.retirement,
                                                                           average_nps,
                                                                           average_retirement,
                                                                           indicators.redflags,
                                                                           actual_sem_flag=actual_sem_flag)

        return indicators_message
    return


def get_right_keyboard(prep):
    pointer = prep.sem_pointer

    there_is_ahead_flag = len(semesters_names) > pointer + 1 and \
                          prep.semesters_indicators[semesters_names[pointer + 1]] and \
                          any(prep.semesters_indicators[semesters_names[pointer + 1]])
    there_is_behind_flag = pointer > 0 and \
                           prep.semesters_indicators[semesters_names[pointer - 1]] and \
                           any(prep.semesters_indicators[semesters_names[pointer - 1]])

    if there_is_ahead_flag and there_is_behind_flag:
        return double_keyboard
    if there_is_ahead_flag:
        return next_keyboard
    if there_is_behind_flag:
        return prev_keyboard

    return None


def get_indicators_action(update: Update, context: CallbackContext) -> None:
    message = update.message.reply_text('Секундочку, чичас поищу')

    prep = Prep(update.effective_user.id, update.effective_user.name)
    if prep.status == "Работает – ассистент":
        message.edit_text("Уважаемый асисстент, сейчас у вас нет грейда. Он у вас появится, "
                          "когда вы обмотаетесь в кокон и превратитесь в прекрасного преподавателя 🦋")
        return

    sem = semesters_names[prep.sem_pointer]
    final_message = f"*Семестр {sem}\n\n\n*"

    final_message = final_message + get_indicators(prep) + \
                    messenger.grade_info_message(
                        prep.semesters_indicators[sem].grade, actual_sem=(sem == ACTUAL_SEM)) + \
                    messenger.current_group_detailing_nps_message(
                        prep.semesters_indicators[
                            sem].group_detailing)

    reply_markup = get_right_keyboard(prep)
    message.edit_text(final_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    logger.info(f"[{prep.prep_tg_name}] got his indicators.")
