import sys

from loguru import logger
from telegram.error import InvalidToken, NetworkError
from telegram.ext import Updater

from shp_mailing_bot.bot import init_dispatcher
from shp_mailing_bot.config import TELEGRAM_BOT_TOKEN


logger.add('debug.log', encoding="utf8", rotation='10 MB', compression='zip')


def main():
    try:
        logger.debug('Запуск')
        logger.debug('Подключение к telegram API...')
        updater = Updater(token=TELEGRAM_BOT_TOKEN)
        logger.info('Подключение к telegram API установлено.')
        init_dispatcher(updater)
        logger.info('Бот запущен')
        updater.start_polling()
        updater.idle()
    except InvalidToken:
        logger.critical('В настройках бота указан некорректный токен. Дальнейшая работа бота невозможна, останов.')
        sys.exit(101)
    except NetworkError:
        logger.critical('Отсутствует подключение к сети интернет. Дальнейшая работа бота невозможна, останов.')
        sys.exit(102)


if __name__ == "__main__":
    main()
