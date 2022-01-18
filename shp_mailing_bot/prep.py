from cachetools import TTLCache

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_prep_indicators import NotionParserPrep
from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_average_indicators import NotionParserAverageMeans
from mailing_bot.shp_mailing_bot.config import ACTUAL_SEM, ttl


class Prep:
    preps_cashed_list = TTLCache(maxsize=200, ttl=ttl)

    _average_indicators = NotionParserAverageMeans().read_database()
    average_curr_nps = _average_indicators.get_field_info(f"NPS {ACTUAL_SEM}")
    average_curr_retirement = _average_indicators.get_field_info(f"Выбываемость {ACTUAL_SEM}")
    del _average_indicators

    def __init__(self, prep_id):
        self.prep_id = prep_id
        info = NotionParserPrep(prep_id).read_database()
        self.nps_curr = info.get_field_info(f"NPS {ACTUAL_SEM}")
        self.retirement_curr = info.get_field_info(f"Выбываемость {ACTUAL_SEM}")
        self.redflags_curr = info.get_field_info(f"Рэдфлаги {ACTUAL_SEM}")

    def get_curr_nps(self):
        return self.nps_curr

    def get_curr_retirement(self):
        return self.retirement_curr

    def get_curr_redflags(self):
        return self.redflags_curr
