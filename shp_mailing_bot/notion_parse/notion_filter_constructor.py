from logger_bot import logger


class FilterConstructor:
    def __init__(self, tg_id, tg_username):
        self.tg_id: int = tg_id
        self.tg_username: str = tg_username
        self.base_filter = {}

    def create_filter(self) -> dict:
        self.construct()
        logger.info(self.base_filter)
        return self.base_filter

    def construct(self):
        if self.tg_id:
            logger.info(f"Here tg id: {self.tg_id}")
            self.add_tg_id_to_filter()
            return
        else:
            logger.warning(f"No tg id for user {self.tg_username}")

    def add_tg_id_to_filter(self):
        self.base_filter["filter"] = {"property": "Telegram ID",
                                      "number": {"equals": self.tg_id}}
