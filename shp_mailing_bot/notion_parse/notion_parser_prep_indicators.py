from loguru import logger
import cachetools.func

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser import NotionParser
from mailing_bot.shp_mailing_bot.config import ACTUAL_SEM, ttl

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')


class NotionParserPrep(NotionParser):
    def __init__(self, prep_id):
        super().__init__(prep_id)

    @cachetools.func.ttl_cache(ttl=ttl)
    def get_field_info(self, field: str = f"NPS {ACTUAL_SEM}"):
        if not self.prep_info:
            return None
        if field not in self.prep_info.keys():
            return None
        state = self._find_field_meaning("Статус", self.prep_info)
        if not state or state == "Уволен":
            return None
        return self._find_field_meaning(field, self.prep_info)

