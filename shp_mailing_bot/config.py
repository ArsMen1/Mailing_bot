import os
from dotenv import load_dotenv

load_dotenv()
# Environment config
CNC_SPREADSHEET_ID = os.getenv('CNC_SPREADSHEET_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_TOKEN_TEST = os.getenv('TELEGRAM_BOT_TOKEN_KATE')

# Google Sheets API config
GOOGLE_SHEET_API_AUTH_SCOPE_URL = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CNC_SPREADSHEET_CELLS_RANGE = 'Data!A1:А13'
INDICATORS_SHEET_ID = '1MB_4rDITzIx_WowAvwRhQFD3_U5H5amMbBWIvUCngdU'
INDICATORS_LIST = "Test"

# info for bot
KNOWLEDGE_BASE_LINK = \
    "https://www.notion.so/itc-shp/185484d383dd46b8bc9d2c130693fff3?v=dcfb3fb534cf4ccba3122631d8e54dec"

DB_PHRASES = (
    "Пожалуйста.",
    "Ой! Концентрация пользы на одну маленькую кнопку превышена 🤓",
    "База Знаний обитает тут: ",
    "Вот ссылочка. И больше не теряйте 🙃",
    "Вот же она!",
    "Надеюсь, вы понимаете, что заходите в храм ценнейших знаний ШП. Ведите себя тихо 🤫",
    "Потеряли Базу Знаний? Лаадно, держите 😌",
    "Вот подарочек на Новый Год от меня 🤗️",
    ""
)

EXCELLENT_INDICATORS_COMMENTS = (
    "Кайф :)",
    "Прекрасный результат 🤩",
    "Так держать!",
    "Вау вау 😀",
    "Вас так любят ученики 🥰",
    "Отличные показатели 😌",
    "Ого-го, здорово :)",
    "Замечательные показатели ☺️",
    "Высший пилотаж ✈️",
    "Ничего себе, вот это класс!",
    "Ой, извините, простите, я что, разговариваю с народным любимцем??",
    "А можно ваш автограф?)",
    "Вау, круто 😄",
    "Это история про успех 😎",
    "Образцово-показательный результат)",
    "Юхуу 🤠",
    "Продолжайте в том же духе 🙂",
    "За вами уже выехала полиция за превышения уровня хорошести!!!",
    "Знаете, я хотел бы чтобы меня тоже так кто-нибудь любил как вас любят дети 🥺"
)

GOOD_INDICATORS_COMMENTS = (
    "Хорошие показатели ☺️",
    "Неплохо!",
    "Неплохой результат 🙂",
    "Стабильные показатели, здорово)",
    "Очень неплохо. Дальше — больше 💪",
    ""
)

BAD_INDICATORS_COMMENTS = (
    "Стоит повнимательнее быть к своим ученикам 🥺",
    "Подумайте, в чем может быть дело 🤔",
    "Стоит задуматься, в чем может быть проблема 🙄"
)

TOP_BAR_NPS = 80  # высокий результат -- от 80 и выше
MEDIUM_BAR_NPS = 65  # средний результат от 65 до 80
# низкий результат -- меньше 65

TOP_BAR_RETIREMENT = 3
MEDIUM_BAR_RETIREMENT = 8
