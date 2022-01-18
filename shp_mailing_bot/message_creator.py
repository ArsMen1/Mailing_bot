from random import choice
from mailing_bot.shp_mailing_bot.config import RESPONSIBLE_FOR_THE_BOT

TOP_BAR_NPS = 80  # высокий результат -- от 80 и выше
MEDIUM_BAR_NPS = 65  # средний результат -- от 65 до 80
# низкий результат -- меньше 65

# средний NPS +15 и -10

TOP_BAR_RETIREMENT = 3
MEDIUM_BAR_RETIREMENT = 8


def ok_message() -> str:
    ok_phrases = (
        'Ок',
        'Принято',
        'Всё ясно',
        'Воспринято',
        'Понятно всё',
        'Ага, понятно',
        'Ок, спасибо',
        'Общепонятно',
        'Схвачено',
        'Принято',
        'Доступно',
        'ШПасибо, всё понятно'
    )

    return choice(ok_phrases)


def kd_link_message() -> str:
    DB_PHRASES = (
        'Пожалуйста.',
        'Ой! Концентрация пользы на одну маленькую кнопку превышена 🤓',
        'База Знаний обитает тут: ',
        'Вот ссылочка. И больше не теряйте 🙃',
        'Вот же она!',
        'Надеюсь, вы понимаете, что заходите в храм ценнейших знаний ШП. Ведите себя тихо 🤫',
        'Потеряли Базу Знаний? Лаадно, держите 😌',
        'Знакомьтесь, глубоко уважаемая База Знаньевна ШПвовна📖: ',
        'Вот, не благодарите'
    )

    return choice(DB_PHRASES)


def evaluation_indicator(nps: str = None, retirement: str = None) -> str:  # get comment for nps or retirement
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
    )

    bad_indicators_comment = (
        'Стоит повнимательнее быть к своим ученикам 🥺',
        'Стоит задуматься, в чем может быть проблема 🙄',
        'Можно попробовать поискать ещё подход к ребятам. Непобедимых не бывает 💪',
        'Всегда можно обратиться за помощью :)'
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


def indicators_message(nps: str,
                       retirement: str,
                       average_nps: str,
                       average_retirement: str,
                       redflags: str) -> tuple:
    """
    Returnes a message and an indicators flag (are there indicators or not)
    """

    redflags_message = ''
    if redflags and redflags != "0":
        redflags_message = f'\n\n*Количество редфлагов — {redflags}.*\n' \
                           f'Для уточнения информации по причинам получения рефдлагов ' \
                           f'обратитесь к вашему руководителю.'

    if not nps and not retirement:
        return 'Ой, не могу найти ваши показатели 👉🏻👈🏻\n\n' \
               'Если вы преподаёте первый семестр, то просто дождитесь окончания семестра. ' \
               'Ваши показатели только формируются\n\n' \
               f'В противном случае для добавления показателей в базу обратитесь к {RESPONSIBLE_FOR_THE_BOT}.', \
               False  # indicators flag
    else:
        if nps and retirement:
            nps_evaluation = evaluation_indicator(nps=nps)
            retirement_evaluation = evaluation_indicator(retirement=retirement)

            return f'*Ваш NPS — {nps}*.\n' \
                   f'Средний NPS по школе — {average_nps}.\n' \
                   f'💭 `{nps_evaluation}`\n\n' \
                   f'*Ваша выбываемость — {retirement}*.\n' \
                   f'Средняя выбываемость по школе — {average_retirement}.\n' \
                   f'💭 `{retirement_evaluation}`' + redflags_message, \
                   True  # indicators flag
        elif nps and not retirement:
            return f'*Ваш NPS — {nps}*.\n' \
                   f'Средний NPS по школе — {average_nps}.\n' \
                   f'💭 `{evaluation_indicator(nps=nps)}`\n\n' \
                   'Информации по вашей выбываемости я не нашёл 🧐 \n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}' + \
                   redflags_message, \
                   True  # indicators flag
        elif retirement and not nps:
            return f'*Ваша выбываемость — {retirement}*.\n' \
                   f'Средняя выбываемость по школе — {average_retirement}.\n' \
                   f'💭 `{evaluation_indicator(retirement=retirement)}\n\n`' \
                   'Информации по вашему NPS я не нашёл 🧐\n' \
                   f'Если вы думаете, что это ошибка, пожалуйста, обратитесь к  {RESPONSIBLE_FOR_THE_BOT}' + \
                   redflags_message, \
                   True  # indicators flag


def current_group_detailing_nps_message() -> str:
    return 'Детализация по группам (M203 вы зашли, а А302 считают, что вы отстой)'


def get_current_nps_message() -> str:
    return 'У вас отличная статистика. Чтобы узнать больше, пришлите смс на телефон 150-64-32.'


def grade_info_message() -> str:
    n = ' ' * 8

    return '*Грейд 3:*\n' + \
           n + 'NPS >=83%\n' + \
           n + 'Выбываемость <= 7%\n' + \
           n + '*🤑 Премия — 30%*\n\n' + \
           '*Грейд 2:*\n' + \
           n + 'NPS >= 72%\n' + \
           n + 'Выбываемость <= 10%\n' + \
           n + '*💰 Премия — 15%*\n\n' + \
           '*Грейд 1:*\n' + \
           n + 'NPS  >= 60%\n' + \
           n + 'Выбываемость <= 13%\n' + \
           n + '*💵 Премия — 5%*\n\n' + \
           '*Грейд 0:*\n' + \
           n + 'NPS  < 60%\n' + \
           n + 'Выбываемость > 13%\n' + \
           n + '*💸 Премия — 0%*\n\n' + \
           '*Итоговый грейд — минимальный из двух грейдов по NPS и по выбываемости.*\nНапример, по выбываемости грейд 2, а по NPS — 3. Итоговый грейд — 2.\nТакже на итоговый грейд влияют редфлаги.\n\n' \
           '_За более подробной информацией вы можете заглянуть в статью в Базе Знаний. Ссылка прикреплена к кнопке ниже._'
