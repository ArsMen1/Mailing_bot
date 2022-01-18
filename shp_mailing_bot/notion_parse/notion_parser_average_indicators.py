import cachetools.func
from loguru import logger

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser import NotionParser
from mailing_bot.shp_mailing_bot.config import TG_ID_MEAN_INDICATORS, ACTUAL_SEM, ttl

logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')


class NotionParserAverageMeans(NotionParser):
    def __init__(self):
        super().__init__(TG_ID_MEAN_INDICATORS)

    @cachetools.func.ttl_cache(ttl=ttl)
    def get_field_info(self, field: str = f"NPS {ACTUAL_SEM}"):
        if not self.prep_info:
            return None
        if field not in self.prep_info.keys():
            return None

        return self._find_field_meaning(field, self.prep_info)
