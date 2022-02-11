from random import choice
from re import search, match
from mailing_bot.shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT, GRADE_INFO_STATE_LINK
from tabulate import tabulate
from mailing_bot.logger_bot import logger

TOP_BAR_NPS = 80  # высокий результат -- от 80 и выше
MEDIUM_BAR_NPS = 65  # средний результат -- от 65 до 80
# низкий результат -- меньше 65

# средний NPS +15 и -10

TOP_BAR_RETIREMENT = 4
MEDIUM_BAR_RETIREMENT = 8

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


def evaluation_indicator_message(nps: str = None, retirement: str = None) -> str:  # get comment for nps or retirement
    # phrases
    excellent_indicators_comments = (
        'Кайф :)',
        'Прекрасный результат 🤩',
        'Так держать!',
        'Вау вау 😀',
        'Вас так любят ученики 🥰',
        'Отличные показатели 😌',
        'Ого-го, здорово :)',
        'Замечательные показатели ☺️',
        'Высший пилотаж ✈️',
        'Ничего себе, вот это класс!',
        'Ой, извините, простите, я что, разговариваю с народным любимцем??',
        'А можно ваш автограф?)',
        'Вау, круто 😄',
        'Это история про успех 😎',
        'Образцово-показательный результат)',
        'Юхуу 🤠',
        'Сильно...',
        'Продолжайте в том же духе 🙂',
        'За вами уже выехала полиция за превышение уровня хорошести!!!',
        'Знаете, я хотел бы, чтобы меня тоже так кто-нибудь любил как вас любят дети 🥺'
    )

    good_indicators_comments = (
        'Хорошие показатели ☺️',
        'Неплохо!',
        'Здоровооо',
        'Неплохой результат 🙂',
        'Стабильные показатели, здорово)',
        'Очень неплохо. Дальше — больше 💪',
        'Замечательно!',
    )

    bad_indicators_comment = (
        'Можно попробовать поискать ещё подход к ребятам. Непобедимых не бывает 💪',
        'Всегда можно обратиться за помощью :)',
        'Если вы чувствуете, что вам нужна помощь, вы всегда можете обратиться к любому сотруднику ВУЦ 🙂',
    )

    if nps and nps[-1] == '%':
        nps = float(nps.replace(',', '.')[:-1])
    if retirement and retirement[-1] == '%':
        retirement = retirement.replace(',', '.')[:-1]

    if (nps and nps >= TOP_BAR_NPS) or \
            (retirement and float(retirement) < TOP_BAR_RETIREMENT):
        return choice(excellent_indicators_comments)

    elif (nps and
          MEDIUM_BAR_NPS <= nps < TOP_BAR_NPS) or \
            (retirement and
             MEDIUM_BAR_RETIREMENT > float(retirement) >= TOP_BAR_RETIREMENT):
        return choice(good_indicators_comments)

    elif (nps and nps < MEDIUM_BAR_NPS) or \
            (retirement and float(retirement) >= MEDIUM_BAR_RETIREMENT):
        return choice(bad_indicators_comment)


def get_name_patronymic(name: str):
    name = name.split()
    if len(name) == 3 or len(name) == 4:  # 4 -- could be maiden name
        return " ".join(name[-2:])
    elif len(name) == 2:
        return name[-1]


def indicators_message(nps: str,
                       retirement: str,
                       average_nps: str,
                       average_retirement: str,
                       redflags: str,
                       actual_sem_flag: bool = False) -> tuple:
    """
    Returns a message and an indicators flag (are there indicators or not)
    """

    if not nps and not retirement:
        return 'Ой, не могу найти ваши показатели 👉🏻👈🏻\n\n' \
               'Если вы преподаёте первый семестр, то просто дождитесь окончания семестра. ' \
               'Ваши показатели только формируются\n\n' \
               f'В противном случае для добавления показателей в базу обратитесь к {RESPONSIBLE_FOR_THE_BOT}.', \
               False  # indicators flag

    nps_comment = ""
    retirement_comment = ""

    if actual_sem_flag:
        nps_comment = f'💭 `{evaluation_indicator_message(nps=nps)}`'
        retirement_comment = f'💭 `{evaluation_indicator_message(retirement=retirement)}`'

    message = f'📌 *Показатели*'

    if nps:
        message += f'\n\n' \
                   f'*Ваш NPS — {nps}.*\n' \
                   f'Средний NPS по школе — {average_nps}.\n' + \
                   nps_comment
    else:
        message += '\n\n' \
                   'Информации по вашему NPS я не нашёл в своей книжечке 🧐\n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}'

    if retirement:
        message += f'\n\n' \
                   f'*Ваша выбываемость — {retirement}.*\n' \
                   f'Средняя выбываемость по школе — {average_retirement}.\n' + \
                   retirement_comment
    else:
        message += '\n\n' \
                   'Информации по вашей выбываемости я не нашёл в своей книжечке 🧐\n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}'

    if redflags:
        message += f'\n\n*Количество редфлагов — *{redflags}.\n'

    return message, True


def current_group_detailing_nps_message(info):
    if not info:
        return ""

    result = f"\n\n\n📌 *Детализация по группам*\n\n"

    info = info.split("\n")
    table = []
    for s in info:
        item = s.split("\t")
        # logger.debug(item)
        curse = match(r"[А-Яа-яЁёA-Za-z/+\-]+", item[0])
        if not curse:
            return ""
        # group = search(r"_?\w\d{3}", item[0])
        group = item[0].split("-")
        if not group:
            pass
        item[0] = curse[0] + "-" + group[-2]
        table.append(item)
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
    result = "\n\n*Ваш грейд —  "
    grade = info[:1]
    result += grade + f" {choice(grade_emoji[int(grade)])}" + "*"
    if actual_sem:
        result += f"\nПодробнее о формировании грейда, NPS и редфлагах можете почитать в [этой статье]({GRADE_INFO_STATE_LINK})."
    return result

# def grade_info_message() -> str:
#     n = ' ' * 8
#
#     return '*Грейд 3:*\n' + \
#            n + 'NPS >=83%\n' + \
#            n + 'Выбываемость <= 7%\n' + \
#            n + '*🤑 Премия — 30%*\n\n' + \
#            '*Грейд 2:*\n' + \
#            n + 'NPS >= 72%\n' + \
#            n + 'Выбываемость <= 10%\n' + \
#            n + '*💰 Премия — 15%*\n\n' + \
#            '*Грейд 1:*\n' + \
#            n + 'NPS  >= 60%\n' + \
#            n + 'Выбываемость <= 13%\n' + \
#            n + '*💵 Премия — 5%*\n\n' + \
#            '*Грейд 0:*\n' + \
#            n + 'NPS  < 60%\n' + \
#            n + 'Выбываемость > 13%\n' + \
#            n + '*💸 Премия — 0%*\n\n' + \
#            '*Итоговый грейд — минимальный из двух грейдов по NPS и по выбываемости.*\n' \
#            'Например, по выбываемости грейд 2, а по NPS — 3. \nИтоговый грейд — 2.\n' \
#            'Также на итоговый грейд влияют редфлаги.\n\n' \
#            '_За более подробной информацией вы можете заглянуть в статью в Базе Знаний. ' \
#            'Ссылка прикреплена к кнопке ниже._'
