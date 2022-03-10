import cachetools.func
from collections import namedtuple

from mailing_bot.logger_bot import logger
from mailing_bot.shp_mailing_bot.notion_parse.notion_parser import NotionParser
from mailing_bot.shp_mailing_bot.config import TG_ID_MEAN_INDICATORS, ACTUAL_SEM, semesters_names


class NotionParserAverageMeans(NotionParser):
    def __init__(self):
        super().__init__(TG_ID_MEAN_INDICATORS)

    def get_field_info(self, field: str = f"NPS {ACTUAL_SEM}"):
        if not self.prep_info:
            return None
        if field not in self.prep_info.keys():
            return None

        res = self._find_field_meaning(field)

        return res

    def get_average_indicators(self):
        _average_indicators = self.read_database()
        AverageIndicatorsItem: [namedtuple] = namedtuple("AverageIndicatorsItem", ["nps", "retirement"])
        average_indicators: [dict] = dict.fromkeys(semesters_names)

        for sem in average_indicators.keys():
            average_indicators[sem] = AverageIndicatorsItem(
                _average_indicators.get_field_info(f"NPS {sem}"),
                _average_indicators.get_field_info(f"Выбываемость {sem}"))
        del _average_indicators
        del AverageIndicatorsItem
        logger.debug(f"Added average indicators: {average_indicators}")
        return average_indicators
