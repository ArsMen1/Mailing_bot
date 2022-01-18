from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from mailing_bot.shp_mailing_bot.config import GET_MAIN_MENU_INDICATORS, GET_PREV_SEM_DETAILING, GET_NEXT_SEM_DETAILING
from mailing_bot.shp_mailing_bot.prep import Prep, semesters_names

from loguru import logger

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')

ok_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Ok", callback_data=GET_MAIN_MENU_INDICATORS)]])
prev_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM_DETAILING)],
                                      [InlineKeyboardButton("Ok", callback_data=GET_MAIN_MENU_INDICATORS)]
                                      ])
next_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM_DETAILING)],
                                      [InlineKeyboardButton("Ok", callback_data=GET_MAIN_MENU_INDICATORS)]
                                      ])
double_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Предыдущий", callback_data=GET_PREV_SEM_DETAILING),
                                         InlineKeyboardButton("Следующий", callback_data=GET_NEXT_SEM_DETAILING)],
                                        [InlineKeyboardButton("Ok", callback_data=GET_MAIN_MENU_INDICATORS)]
                                        ])


def get_right_keyboard(prep):
    there_is_ahead_flag = len(semesters_names) > prep.sem_pointer + 1 and \
                          any(prep.semesters_indicators[semesters_names[prep.sem_pointer + 1]])
    there_is_behind_flag = prep.sem_pointer > 0 and any(
        prep.semesters_indicators[semesters_names[prep.sem_pointer - 1]])
    if there_is_ahead_flag and there_is_behind_flag:
        return double_keyboard
    elif there_is_ahead_flag:
        return next_keyboard
    elif there_is_behind_flag:
        return prev_keyboard
    else:
        return ok_keyboard


def get_prep(update):
    prep_id = update.effective_user.id
    if prep_id not in Prep.preps_cashed_list:
        Prep.preps_cashed_list[prep_id] = Prep(prep_id)
    prep = Prep.preps_cashed_list[prep_id]
    prep.get_indicators_semester_statistic()
    return prep


def semesters_navigator(func):
    def wrapper(update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        prep = get_prep(update)

        func(update, context, prep)

        indicators = prep.semesters_indicators[semesters_names[prep.sem_pointer]]
        actual_keyboard = get_right_keyboard(prep)
        query.edit_message_text(f"Семестр: {semesters_names[prep.sem_pointer]}\n"
                                f"NPS: {indicators.nps}\n"
                                f"Выбываемость: {indicators.retirement}\n"
                                f"Редфлаги: {indicators.redflags}",
                                reply_markup=actual_keyboard)

    return wrapper


@semesters_navigator
def get_nps_stat(update, context, prep) -> None:
    pass


@semesters_navigator
def get_nps_stat_next(update, context, prep) -> None:
    prep.sem_pointer += 1


@semesters_navigator
def get_nps_stat_prev(update, context, prep) -> None:
    prep.sem_pointer -= 1
