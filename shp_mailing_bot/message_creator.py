from random import choice
from re import findall
from shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT, GRADE_INFO_STATE_LINK
from tabulate import tabulate
from logger_bot import logger

are_you_really_prep_message = 'Не могу вас найти в моей тетрадочке, вы точно преподаватель? 🥸\n' \
                              f'Если да, то скажите про это моей мамочке {RESPONSIBLE_FOR_THE_BOT}, ' \
                              f'она вас запишет карандашом.'


# def ok_message() -> str:
#     ok_phrases = (
#         'Ок',
#         'Принято',
#         'Всё ясно',
#         'Воспринято',
#         'Понятно всё',
#         'Ага, понятно',
#         'Ок, спасибо',
#         'Общепонятно',
#         'Схвачено',
#         'Принято',
#         'Доступно',
#         'ШПасибо, всё понятно'
#     )
#
#     return choice(ok_phrases)


def kd_link_message() -> str:
    db_phrases = (
        'Пожалуйста.',
        'Ой! Концентрация пользы на одну маленькую кнопку превышена 🤓',
        'База Знаний обитает тут: ',
        'Вот ссылочка. И больше не теряйте 🙃',
        'Вот же она!',
        'Надеюсь, вы понимаете, что заходите в храм ценнейших знаний ШП. Ведите себя тихо 🤫',
        'Потеряли Базу Знаний? Лаадно, держите 😌',
        'Знакомьтесь, наша глубоко уважаемая База Знаньевна ШПвовна ',
        'Вот, не благодарите',
        'Вот он, наш свяой грааль, обращайтесь с ним бережно'
    )

    return choice(db_phrases)


def evaluation_indicator_message(grade: int = None) -> str:  # get comment for nps or retirement

    # phrases
    grade_3_indicators_comment = (
        'Кайф :)',
        'Прекрасный результат 🤩',
        'Вау вау 😀',
        'Вас так любят ученики 🥰',
        'Отличные показатели 😌',
        'Ого-го, здорово :)',
        'Замечательные показатели ☺️',
        'Высший пилотаж ✈️',
        'Ничего себе, вот это класс!',
        'Ой, извините, простите, я что, разговариваю с народным любимцем??',
        'А можно ваш автограф?)',
        'Это история про успех 😎',
        'Образцово-показательный результат)',
        'Юхуу 🤠',
        'Сильно...',
        'Продолжайте в том же духе 🙂',
        'За вами уже выехала полиция за превышение уровня хорошести!!!',
        'Знаете, я хотел бы, чтобы меня тоже так кто-нибудь любил как вас любят дети 🥺'
    )

    grade_2_indicators_comment = (
        'Хорошие показатели ☺️',
        'Неплохо!',
        'Здоровооо',
        'Чудесно!',
        'Неплохой результат 🙂',
        'Стабильные показатели, здорово)',
        'Очень неплохо. Дальше — больше 💪',
        'Замечательно!',
        'Так держать!',
        "Качественная работа!",
        'Вау, круто 😄',
        "Сильно..."
    )

    grade_1_indicators_comment = (
        "Неплохо! Дальше — больше 💪",
        "Неплохой результат :)",
        "Хороший результат! И прекрасно здесь то, что есть место для роста :)"
    )

    grade_0_indicators_comment = (
        'Можно попробовать поискать ещё подход к ребятам. Непобедимых не бывает 💪',
        'Всегда можно обратиться за помощью :)',
        'Если вы чувствуете, что вам нужна помощь, вы всегда можете обратиться к любому сотруднику ВУЦ 🙂',
        "Прекрасно здесь то, что есть место для роста 😄"
    )

    comments_grade = (
        grade_0_indicators_comment, grade_1_indicators_comment, grade_2_indicators_comment, grade_3_indicators_comment)

    return choice(comments_grade[grade])


def get_name_patronymic(name: str):
    name = name.split()
    if len(name) == 3 or len(name) == 4:  # 4 -- could be maiden name
        return " ".join(name[-2:])
    elif len(name) == 2:
        return name[-1]


def indicators_message(nps: str,
                       positive: str,
                       negative: str,
                       neutral: str,
                       retirement: str,
                       average_nps: str,
                       average_retirement: str,
                       redflags: str,
                       sem_pointer) -> str:
    """
    Returns a message and an indicators flag (are there indicators or not)
    """

    # nps_comment = ""
    # retirement_comment = ""
    #
    # if actual_sem_flag:
    #     nps_comment = f'💭 `{evaluation_indicator_message(nps=nps)}`'
    #     retirement_comment = f'💭 `{evaluation_indicator_message(retirement=retirement)}`'

    message = f'📌 *Показатели*'

    if nps:
        message += f'\n\n' \
                   f'*Ваш NPS — {nps}%.*\n' \
                   f'Средний NPS по школе — {average_nps}%.\n'
    else:
        message += '\n\n' \
                   'Информации по вашему NPS я не нашёл в своей книжечке 🧐\n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}'

    if any((positive, negative, neutral)):
        message += f"\nГолоса распределились так:\n" \
                   f"`положительные — {positive}\n" \
                   f"отрицательные — {negative}\n" \
                   f"нейтральные   — {int(neutral) + int(retirement)}\n" \
                   f"(из них {retirement} прекратили обучение в школе)`"

    if retirement and sem_pointer < 6:  # if sem 21/22-I and +
        message += f'\n\n' \
                   f'*Ваша выбываемость — {retirement}%.*\n' \
                   f'Средняя выбываемость по школе — {average_retirement}%.\n'
    elif sem_pointer < 6:
        message += '\n\n' \
                   'Информации по вашей выбываемости я не нашёл в своей книжечке 🧐\n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}'

    if redflags:
        message += f'\n\n*Количество редфлагов — *{redflags}.\n'
    return message


def current_group_detailing_nps_message(info):
    if not info:
        logger.info("No group detailing info.")
        return ""

    result = f"\n\n\n📌 *Детализация по группам*\n\n"
    info = info.split("\n")
    table = []
    groups_re = \
        r'^((?:\-[a-zA-Z]|[\s\/+a-zA-ZА-Яа-яёЁ])+)(?:-\d)?(?:_base_\d*|_spec_\d*)?(?:[_\w,]+?)?-((?:\w+,?)+)-(?:(\d\d/\d\d)|(\d\d)).*$'
    for line in info:
        # line = [FORMAT_base_1-M204-21/22-I\t90,54%]
        if line == "":
            continue
        line = line.split("\t")
        group = findall(groups_re, line[0])
        logger.debug(group)
        logger.debug(line)
        table.append((f"{group[0][0]}—{group[0][1]}", line[1]))
    result = result + "`" + tabulate(table, headers=["Группа", "NPS"]) + "`"

    return result


grade_3_emoji = "😃😄😁😀🥰😍🤠"
grade_2_emoji = "🙂🙃😊😌🤗😉"
grade_1_emoji = "🤨🥸🧐😶🤔🙄"
grade_0_emoji = "😔😒😕🙁😓😶😵‍💫"
grade_emoji = (grade_0_emoji, grade_1_emoji, grade_2_emoji, grade_3_emoji)

def grade_info_message(info, actual_sem=False):
    if not info:
        return ""
    grade = info[0]
    if int(grade) != 0:
        result = f"\n\n*У вас премия {grade} категории.* "
    else:
        result = f"\n\n*К сожалению, вы не получили премию в этом семестре.*"
    if actual_sem:
        result += f"\n" \
                  f"💭 `{evaluation_indicator_message(grade=int(grade))}`"
        result += f"\n[Статья о том, как формируются показатели]" \
                  f"({GRADE_INFO_STATE_LINK})."
    return result
