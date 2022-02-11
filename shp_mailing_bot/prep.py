from cachetools import TTLCache
from collections import namedtuple

from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_prep_indicators import NotionParserPrep
from mailing_bot.shp_mailing_bot.notion_parse.notion_parser_average_indicators import NotionParserAverageMeans
from mailing_bot.shp_mailing_bot.config import ttl, semesters_names
from mailing_bot.logger_bot import logger


class Prep:
    preps_cashed_list = TTLCache(maxsize=200, ttl=ttl)
    average_indicators = NotionParserAverageMeans().get_average_indicators()
    # getting average indicators for each semester
    # _average_indicators = NotionParserAverageMeans().read_database()
    # AverageIndicatorsItem: [namedtuple] = namedtuple("AverageIndicatorsItem", ["nps", "retirement"])
    # average_indicators: [dict] = dict.fromkeys(semesters_names)

    # for sem in average_indicators.keys():
    #     average_indicators[sem] = AverageIndicatorsItem(
    #         _average_indicators.get_field_info(f"NPS {sem}"),
    #         _average_indicators.get_field_info(f"Выбываемость {sem}"))
    # del _average_indicators
    # del AverageIndicatorsItem

    def __new__(cls, prep_id: int, tg_name: str):
        if prep_id not in cls.preps_cashed_list:
            cls.preps_cashed_list[prep_id] = super().__new__(cls)
        prep = cls.preps_cashed_list[prep_id]

        return prep

    def __init__(self, prep_id, tg_name: str):
        if hasattr(self, "id"):
            logger.debug(f"[{self.tg_name}] exists already, go on.")
            return
        self.id: int = prep_id
        self.tg_name: str = tg_name
        self.info: [NotionParserPrep] = NotionParserPrep(self.id, self.tg_name).read_database()
        self.status: str = self.info.get_field_info("Статус")
        self.does_exists: bool = bool((self.status != "Уволен") and self.info)
        if not self.does_exists:
            logger.debug(f"[{self.tg_name}] is {self.status}, {self.info=}. His instance is None. That's what I say.")
            return
        self.name: str = self.info.get_field_info("Преподаватель")
        if self.status == "Работает – ассистент":
            return
        self.IndicatorsItem: [namedtuple] = namedtuple("IndicatorsItem",
                                                       ["nps",
                                                        "retirement",
                                                        "redflags",
                                                        "group_detailing",
                                                        "grade"])
        self.semesters_indicators: [dict] = dict.fromkeys(semesters_names)
        self.sem_pointer: [int] = len(semesters_names) - 1

        for sem in self.semesters_indicators.keys():
            sem_info = self.IndicatorsItem(
                self.info.get_field_info(f"NPS {sem}"),
                self.info.get_field_info(f"Выбываемость {sem}"),
                self.info.get_field_info(f"Редфлаги {sem}"),
                self.info.get_field_info(f"Детализация {sem}"),
                self.info.get_field_info(f"Грейд {sem}"))
            if any(sem_info):
                self.semesters_indicators[sem] = sem_info
        logger.debug(f"[{self.tg_name}] created prep instance.")

        """
        Turns self.semester_indicators into something like that:
        {'20/21-II': IndicatorsItem(nps='87,30%', retirement='4,00%', redflags=None),
        '20/21-I': IndicatorsItem(nps='84,85%', retirement='9,68%', redflags=None),
        '19/20-II': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '19/20-I': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '18/19-II': IndicatorsItem(nps=None, retirement=None, redflags=None),
        '18/19-I': IndicatorsItem(nps=None, retirement=None, redflags=None)}
        """
