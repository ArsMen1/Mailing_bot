from requests import request
import mailing_bot.shp_mailing_bot.config as config
from json import dump
from loguru import logger

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')


class NotionParser:
    def __init__(self, prep_id: int = None):
        self.response = None
        self.prep_id = prep_id
        self.prep_info = None
        self.database_id = config.database_id_history_of_indicators
        self.token = config.token
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }
        self.body = {"filter":
                         {"property": "Telegram ID", "number": {"equals": self.prep_id}},
                     }

    def read_database(self):
        read_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        res = request("POST", read_url, headers=self.headers, json=self.body)
        self.response = res.json()

        if res.status_code != 200:
            logger.debug(f"{res.status_code=} for user {self.prep_id}")
            logger.debug(f"{self.response}")
            self.response = None

        if "properties" in self.response["results"][0]:
            self.prep_info = self.response["results"][0]["properties"]
        # with open('./db.json', 'w', encoding='utf8') as f:
        #     dump(self.response, f, ensure_ascii=False)
        return self

    @staticmethod
    def _find_field_meaning(field: str, data: dict):
        if not data:
            logger.debug("No data")
            return None
        if field not in data.keys():
            logger.debug(f"[field] not in data.keys()")
        field_type = data[field]["type"]

        if field_type == "rich_text":  # text
            if data[field]["rich_text"] and \
                    "plain_text" in data[field]["rich_text"][0]:
                return data[field]["rich_text"][0]["plain_text"]
            else:
                return None

        elif field_type == "rollup":  # rollup
            if data[field]["rollup"]["array"] and \
                    data[field]["rollup"]["array"][0]["type"] == "select" and \
                    data[field]["rollup"]["array"][0][
                        "select"]:  # if field type -- select if field is not empty
                return data[field]["rollup"]["array"][0]["select"]["name"]

        elif field_type == "select":  # select, if field is empty, it will not be sent
            return data[field]["select"]["name"]

        elif field_type == "number":  # number, if field is empty, it will not be sent
            return data[field]["number"]


