from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from typing import Union

from shp_mailing_bot.config import GET_PREV_SEM, GET_NEXT_SEM, ACTUAL_SEM
import shp_mailing_bot.message_creator as messenger
from shp_mailing_bot.prep import Prep, semesters_names
from shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT
from logger_bot import logger

prev_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий семестр", callback_data=GET_PREV_SEM)]
                                      ])
next_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Следующий семестр", callback_data=GET_NEXT_SEM)]
                                      ])
double_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM),
                                         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM)]
                                        ])


def is_there_sem_ahead(prep):
    pointer = prep.sem_pointer

    for i in range(1, len(semesters_names) - pointer):
        if len(semesters_names) > pointer + i \
                and prep.semesters_indicators[semesters_names[pointer + i]] \
                and any(prep.semesters_indicators[semesters_names[pointer + i]]):
            return True


def is_there_sem_behind(prep):
    pointer = prep.sem_pointer

    for i in range(1, pointer):
        if pointer > 0 \
                and prep.semesters_indicators[semesters_names[pointer - i]] \
                and any(prep.semesters_indicators[semesters_names[pointer - i]]):
            return True


def get_indicators(prep: Prep) -> Union[str, None]:
    sem = semesters_names[prep.sem_pointer]
    indicators = prep.semesters_indicators[sem]

    average_nps, average_retirement = prep.average_indicators[sem]
    if not any(prep.semesters_indicators[sem]):
        if not is_there_sem_behind(prep):
            return 'Ой, в моей книжечке ваших показателей нет 👉🏻👈🏻\n\n' \
                   'Если вы преподаёте первый семестр, то просто дождитесь окончания семестра. ' \
                   'Ваши показатели только формируются\n\n' \
                   f'Если вы думаете, что тут какая-то ошибка, то обратитесь к {RESPONSIBLE_FOR_THE_BOT}.'
        else:
            return "Тут ничего нет и не было 😶‍🌫️"
    else:
        return messenger.indicators_message(indicators.nps,
                                            indicators.positive,
                                            indicators.neutral,
                                            indicators.negative,
                                            indicators.retirement,
                                            average_nps,
                                            average_retirement,
                                            indicators.redflags,
                                            sem_pointer=prep.sem_pointer)


def get_right_keyboard(prep):
    there_is_ahead_flag = is_there_sem_ahead(prep)
    there_is_behind_flag = is_there_sem_behind(prep)

    if there_is_ahead_flag and there_is_behind_flag:
        return double_keyboard
    if there_is_ahead_flag:
        return next_keyboard
    if there_is_behind_flag:
        return prev_keyboard

    return None


def get_actual_sem_indicators(prep):
    if prep.sem_pointer+1 > len(semesters_names) or prep.sem_pointer < 0:
        return "Повторите запрос, пожалуйста, что-то я запутался :("
    sem = semesters_names[prep.sem_pointer]
    final_message = f"*Семестр {sem}\n\n\n*"

    return final_message + get_indicators(prep) + \
           messenger.grade_info_message(
               prep.semesters_indicators[sem].grade, actual_sem=(sem == ACTUAL_SEM)) + \
           messenger.current_group_detailing_nps_message(
               prep.semesters_indicators[
                   sem].group_detailing) + \
           messenger.grade_state_message()


def get_indicators_action(update: Update, context: CallbackContext) -> None:
    message = update.message.reply_text('Секундочку, чичас поищу')
    prep = Prep(update.effective_user.id, update.effective_user.name)
    if not prep.status:
        message.edit_text(messenger.are_you_really_prep_message)
    if prep.status and prep.status == "Работает – ассистент":
        message.edit_text("Уважаемый асисстент, сейчас у вас нет грейда. Он у вас появится, "
                          "когда вы обмотаетесь в кокон и превратитесь в прекрасного преподавателя 🦋")
        return
    final_message = get_actual_sem_indicators(prep)

    reply_markup = get_right_keyboard(prep)
    message.edit_text(final_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
