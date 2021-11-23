import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google.auth.exceptions import TransportError

from mailing_bot.shp_mailing_bot.config import GOOGLE_SHEET_API_AUTH_SCOPE_URL

# При изменении адреса в этой переменной - удалите фал token.json
SCOPES = [GOOGLE_SHEET_API_AUTH_SCOPE_URL]


def authorize():
    """
    Авторизация в гугл-таблицах.
    Возвращает инстанс таблиц в случае успешной авторизации
    """
    credentials = None

    # Сначала пытаемся получить данные из файла token.json. В нём хранятся данные после первой авторизации
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Если такого файла нет - пытаемся залогиниться
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except TransportError as ex:
                print(f"Ошибка {ex}")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        # Сохраняем данные авторизации в файл token.json
        with open('../token.json', 'w') as token:
            token.write(credentials.to_json())

    # Собираем инстанс таблиц
    return build('sheets', 'v4', credentials=credentials)
