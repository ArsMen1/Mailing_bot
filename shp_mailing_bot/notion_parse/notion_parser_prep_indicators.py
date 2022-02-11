import cachetools.func

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser import NotionParser
from mailing_bot.shp_mailing_bot.config import ACTUAL_SEM
from mailing_bot.logger_bot import logger


class NotionParserPrep(NotionParser):
    def __init__(self, prep_id: int, tg_name: str):
        super().__init__(prep_id)
        self.prep_tg_name = tg_name

    def get_field_info(self, field: str = f"NPS {ACTUAL_SEM}"):
        if not self.prep_info:
            logger.debug(f"[{self.prep_tg_name}] no info about him. Return None")
            return None
        if field not in self.prep_info.keys():
            logger.debug(f"[{self.prep_tg_name}] no info for {field=}")
            return None

        res = self._find_field_meaning(field, self.prep_info)
        logger.info(f"[{self.prep_tg_name}] {field} = {res}")

        return res
