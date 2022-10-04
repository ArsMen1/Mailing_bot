import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_TOKEN_TEST = os.getenv('TELEGRAM_BOT_TOKEN_KATE')
NOTION_BOT_TOKEN = os.getenv('NOTION_BOT_TOKEN')

KNOWLEDGE_BASE_LINK = 'https://www.notion.so/mshp/185484d383dd46b8bc9d2c130693fff3?v=dcfb3fb534cf4ccba3122631d8e54dec'
GRADE_INFO_STATE_LINK = 'https://www.notion.so/mshp/NPS-7b1081b7e47d48dbb58c81adc1aa5acc'
LESSON_CONSTRUCTOR_MD = 'https://docs.google.com/spreadsheets/d/1eA12VMO1uHlp-ZeTI62DH8hXD_lOPlbjPkOPeAqMv0k/edit#gid=0'
LESSON_CONSTRUCTOR_JA = 'https://docs.google.com/spreadsheets/d/1oZhZYOKEyOuLJtm15ue2ddiTtaI1jqA4D20aABuK1fo/edit#gid=1141170697'
CONSTRUCTOR_SUGGESTIONS_FORM_LINK = "https://forms.gle/5K9kNNCwb7h4fCzg6"

# data for notion api
database_id_history_of_indicators = "0223e0cec25b4509b0b21daf28a01c1c"
TG_ID_MEAN_INDICATORS = 1000000  # tg id for getting average meanings

semesters_names = ["18/19-I", "18/19-II", "19/20-I", "19/20-II", "20/21-I", "20/21-II", "21/22-I", "21/22-II"]
# change it every semester
ACTUAL_SEM = semesters_names[len(semesters_names) - 1]
RESPONSIBLE_FOR_THE_BOT = "@ktrntrsv"

GET_KD_LINK_BUTTON = 'База знаний'
GET_CURR_SEM = 'Показатели'
GET_NEXT_SEM = "Следующий семестр"
GET_PREV_SEM = "Прошлый семестр"

ttl = 5 * 60  # ttl - seconds
