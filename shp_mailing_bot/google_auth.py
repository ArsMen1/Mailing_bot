import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from shp_mailing_bot.config import GOOGLE_SHEET_API_AUTH_SCOPE_URL

# If modifying these scopes, delete the file token.json.
SCOPES = [GOOGLE_SHEET_API_AUTH_SCOPE_URL]


def authorize():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    credentials = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    service = build('sheets', 'v4', credentials=credentials)
    return service


# Используется только один раз для получения файла token.json
if __name__ == '__main__':
    authorize()
