from mailing_bot.shp_mailing_bot.config import CNC_SPREADSHEET_CELLS_RANGE, CNC_SPREADSHEET_ID, INDICATORS_SHEET_ID, \
    INDICATORS_LIST
from mailing_bot.shp_mailing_bot.google_auth import authorize


def get_values_from_sheet() -> list:
    service = authorize()

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=INDICATORS_SHEET_ID, range=f'{INDICATORS_LIST}!A2:E1000').execute()
    values = result.get('values', [])
    return values
