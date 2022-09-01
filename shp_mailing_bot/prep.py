from cachetools import TTLCache
from collections import namedtuple

from shp_mailing_bot.notion_parse.notion_parser_prep_indicators import NotionParserPrep
from shp_mailing_bot.notion_parse.notion_parser_average_indicators import NotionParserAverageMeans
from shp_mailing_bot.config import ttl, semesters_names
from logger_bot import logger


class Prep:
    preps_cashed_list = TTLCache(maxsize=200, ttl=ttl)
    average_indicators = NotionParserAverageMeans().get_average_indicators()

    def __new__(cls, prep_id: int, prep_tg_name: str):
        if prep_id not in cls.preps_cashed_list:
            cls.preps_cashed_list[prep_id] = super().__new__(cls)
        prep = cls.preps_cashed_list[prep_id]

        return prep

    def __init__(self, prep_id, prep_tg_name: str):
        if hasattr(self, "id"):
            logger.debug(f"[{self.prep_tg_name}] exists already, go on.")
            return
        self.id: int = prep_id
        self.prep_tg_name: str = prep_tg_name
        self.info: [NotionParserPrep] = NotionParserPrep(self.id, self.prep_tg_name).read_database()
        if not self.info:
            self.status = None
            return
        self.status: str = self.info.get_field_info("Статус")
        self.does_exists: bool = bool((self.status != "Больше не работает в компании") and self.info)
        if not self.does_exists:
            logger.debug(
                f"[{self.prep_tg_name}] is {self.status}, {self.info=}. His instance is None. That's what I say.")
            return
        self.name: str = self.info.get_field_info("Преподаватель")
        if self.status == "Работает – ассистент":
            return
        self.IndicatorsItem: [namedtuple] = namedtuple("IndicatorsItem",
                                                       ["nps",
                                                        "positive",
                                                        "negative",
                                                        "neutral",
                                                        "retirement",
                                                        "redflags",
                                                        "group_detailing",
                                                        "grade"])
        self.semesters_indicators: [dict] = dict.fromkeys(semesters_names)
        # self.semesters_indicators={'18/19-I': None, '18/19-II': None, '19/20-I': None...}

        self.sem_pointer: [int] = len(semesters_names) - 1

        self._create_indicators_storage()

    def _create_indicators_storage(self):
        for sem in self.semesters_indicators.keys():

            votes_detailing = self.info.get_field_info(f"Детализация по голосам {sem}")
            if not votes_detailing:
                votes_detailing = [None] * 4
                # logger.info(f"[{self.prep_tg_name}] has no nps percent detailing.")
            else:
                votes_detailing = votes_detailing.split()
                # logger.debug(votes_detailing)

            sem_info = self.IndicatorsItem(
                self.info.get_field_info(f"NPS {sem}"),
                votes_detailing[0],
                votes_detailing[1],
                votes_detailing[2],
                self.info.get_field_info(f"Выбываемость {sem}"),
                self.info.get_field_info(f"Редфлаги {sem}"),
                self.info.get_field_info(f"Детализация по группам {sem}"),
                self.info.get_field_info(f"Грейд {sem}"))
            self.semesters_indicators[sem] = sem_info
            logger.debug(f"{sem_info=}")
        logger.debug(f"[{self.prep_tg_name}] created prep instance.")

        """
        self.semester_indicators into something like that:
        {'20/21-II': IndicatorsItem(nps='87,30%', retirement='4,00%', redflags=None),
        '20/21-I': IndicatorsItem(nps='84,85%', retirement='9,68%', redflags=None)...}
        """
