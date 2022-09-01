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
        if self.tg_username and self.tg_username.startswith("@"):
            logger.info(f"Here username: {self.tg_username}")
            self.add_username_to_filter()
            return
        if self.tg_id:
            logger.info(f"Here tg id: {self.tg_id}")
            self.add_tg_id_to_filter()

    def add_username_to_filter(self):
        self.base_filter["filter"] = {"or": [{"property": "Telegram username",
                                              "rollup": {
                                                  "any": {
                                                      "text": {
                                                          "equals": self.tg_username
                                                      }
                                                  }
                                              }
                                              },
                                             {"property": "Telegram username",
                                              "rollup": {
                                                  "any": {
                                                      "text": {
                                                          "equals": self.tg_username[1:]
                                                      }
                                                  }
                                              }}]}

    def add_tg_id_to_filter(self):
        self.base_filter["filter"] = {"property": "Telegram ID",
                                      "number": {"equals": self.tg_id}}
