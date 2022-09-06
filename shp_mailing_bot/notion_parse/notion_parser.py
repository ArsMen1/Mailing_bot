from requests import request
import shp_mailing_bot.config as config
from logger_bot import logger
from json import dump
from shp_mailing_bot.notion_parse.notion_filter_constructor import FilterConstructor


class NotionParser:
    def __init__(self, prep_id: int, tg_name: str = ""):
        self.response = None
        self.prep_id = prep_id
        self.prep_info = None
        self.tg_name = tg_name
        self.database_id = config.database_id_history_of_indicators
        self.token = config.NOTION_BOT_TOKEN
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }
        self.body = FilterConstructor(self.prep_id, self.tg_name).create_filter()

    def read_database(self):
        read_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        res = request("POST", read_url, headers=self.headers, json=self.body)
        self.response = res.json()

        logger.info(f"{res.json()=}")
        if res.status_code != 200:
            logger.error(f"{res.status_code=} for user {self.prep_id}")
            logger.info(f"{self.response}")
            self.response = None

        if not self.response or not self.response["results"]:
            return
        if "properties" in self.response["results"][0]:
            self.prep_info = self.response["results"][0]["properties"]

        logger.debug(f"I have read a database: {self.prep_info}")
        return self

    def _find_field_meaning(self, field: str):
        if not self.prep_info:
            logger.debug("No data")
            return None
        if field not in self.prep_info.keys():
            logger.debug(f"[field] not in self.prep_info.keys(). {self.prep_info.keys()=} only :(")
        field_type = self.prep_info[field]["type"]

        if field_type == "rich_text":  # text
            if self.prep_info[field]["rich_text"] and "plain_text" in self.prep_info[field]["rich_text"][0]:
                return self.prep_info[field]["rich_text"][0]["plain_text"]
            logger.debug(f"[{self.tg_name}]  no info for {field}, crab")
            return None

        elif field_type == "title":
            if self.prep_info[field]["title"]:
                return self.prep_info[field]["title"][0]["plain_text"]
            logger.debug(f"[{self.tg_name}] there is no title {field=}, he looks like anonymous")
            return None

        elif field_type == "relation":
            if not len(self.prep_info[field]["relation"]):
                return
            return self.prep_info[field]["relation"]

        elif field_type == "rollup":  # rollup
            if self.prep_info[field]["rollup"]["array"] and \
                    self.prep_info[field]["rollup"]["array"][0]["type"] == "select" and \
                    self.prep_info[field]["rollup"]["array"][0][
                        "select"]:  # if field type -- select if field is not empty
                return self.prep_info[field]["rollup"]["array"][0]["select"]["name"]
            logger.debug(f"[{self.tg_name}] no data in rollup about it {field=}")
            return None

        elif field_type == "select":  # select, if field is empty, it will not be sent
            return self.prep_info[field]["select"]["name"]

        elif field_type == "number":  # number, if field is empty, it will not be sent
            return self.prep_info[field]["number"]

        elif field_type == "formula" and self.prep_info[field][field_type]["type"] == "string":
            return self.prep_info[field][field_type]["string"]
