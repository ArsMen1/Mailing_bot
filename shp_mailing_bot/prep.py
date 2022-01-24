from cachetools import TTLCache
from collections import namedtuple
from typing import Union

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_prep_indicators import NotionParserPrep
from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_average_indicators import NotionParserAverageMeans
from mailing_bot.shp_mailing_bot.config import ACTUAL_SEM, ttl, semesters_names


# semesters_names = ["18/19-I", "18/19-II", "19/20-I", "19/20-II", "20/21-I", "20/21-II"]


class Prep:
    preps_cashed_list = TTLCache(maxsize=200, ttl=ttl)

    _average_indicators = NotionParserAverageMeans().read_database()
    average_curr_nps = _average_indicators.get_field_info(f"NPS {ACTUAL_SEM}")
    average_curr_retirement = _average_indicators.get_field_info(f"Выбываемость {ACTUAL_SEM}")
    del _average_indicators

    def __init__(self, prep_id):
        self.prep_id: [int] = prep_id
        self.info: [NotionParserPrep] = NotionParserPrep(prep_id).read_database()
        self.status = None  # todo: think about replacing does_exists
        self.does_exists = bool(self.info)
        if not self.does_exists:
            return
        self.curr_nps: Union[str, None] = None
        self.curr_retirement: Union[str, None] = None
        self.curr_redflags: Union[str, None] = None

        self.group_detailing: Union[str, None] = None

        self.IndicatorsItem: [namedtuple] = namedtuple("IndicatorsItem", ["nps", "retirement", "redflags"])
        self.semesters_indicators: [dict] = dict.fromkeys(semesters_names)
        self.sem_pointer: [int] = len(semesters_names) - 1

    def get_curr_indicators(self):
        self.curr_nps = self.info.get_field_info(f"NPS {ACTUAL_SEM}")
        self.curr_retirement = self.info.get_field_info(f"Выбываемость {ACTUAL_SEM}")
        self.curr_redflags = self.info.get_field_info(f"Рэдфлаги {ACTUAL_SEM}")

        return self.curr_nps, self.curr_retirement, self.curr_redflags

    def get_group_detailing(self):
        self.group_detailing = self.info.get_field_info(f"Детализация {ACTUAL_SEM}")

        return self.group_detailing

    def get_indicators_semester_statistic(self):
        """
        Turns self.semester_indicators into something like that:
        {'20/21-II': IndicatorsItem(nps='87,30%', retirement='4,00%', redflags=None),
        '20/21-I': IndicatorsItem(nps='84,85%', retirement='9,68%', redflags=None),
        '19/20-II': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '19/20-I': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '18/19-II': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '18/19-I': IndicatorsItem(nps=None, retirement=None, redflags=None)}

        """
        for sem in self.semesters_indicators.keys():
            self.semesters_indicators[sem] = self.IndicatorsItem(
                self.info.get_field_info(f"NPS {sem}"),
                self.info.get_field_info(f"Выбываемость {sem}"),
                self.info.get_field_info(f"Редфлаги {sem}"))

    @classmethod
    def find_prep(cls, update):
        prep_id = update.effective_user.id
        if prep_id not in cls.preps_cashed_list:
            cls.preps_cashed_list[prep_id] = cls(prep_id)
        prep = cls.preps_cashed_list[prep_id]
        prep.get_indicators_semester_statistic()
        if prep.info:
            return prep
        else:
            return None
