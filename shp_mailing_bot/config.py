import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_TOKEN_TEST = os.getenv('TELEGRAM_BOT_TOKEN_KATE')

KNOWLEDGE_BASE_LINK = \
    'https://www.notion.so/itc-shp/185484d383dd46b8bc9d2c130693fff3?v=dcfb3fb534cf4ccba3122631d8e54dec'

GRADE_ARTICLE_KB = 'https://www.notion.so/itc-shp/NPS-7b1081b7e47d48dbb58c81adc1aa5acc'

# data for notion api
database_id_history_of_indicators = "0223e0cec25b4509b0b21daf28a01c1c"
token = "secret_sfrairxppAIkYw7WKXMF7xKOgP4DLm3FH6o22XmWC8M"
TG_ID_MEAN_INDICATORS = 1000000  # телеграм id для получения среднего значения

ACTUAL_SEM = "20/21-II"  # change it every semester
RESPONSIBLE_FOR_THE_BOT = "@ktrntrsv"

GET_KD_LINK_BUTTON = 'База знаний'
GET_INDICATORS_BUTTON = 'Мои показатели'
GET_MAIN_MENU_INDICATORS = 'Главное меню'
GET_GROUP_DETAILING_NPS_BUTTON = 'NPS по группам'
GET_SEMESTERS_DETAILING_BUTTON = 'NPS по семестрам'
GET_GRADE_INFO_BUTTON = 'Грейд'

ttl = 10 * 60  # ttl - seconds
