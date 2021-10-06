# SHP Mailing Bot

Telegram-бот для рассылки сообщений преподавателям Московской Школы Программистов.

### Функционал
- Получение списка сообщений и адресатов из google-таблицы
- Batch-отправка их по адресатам.

### Технологический стек
- python-telegram-bot
- google-api-python-client

### Первичная настройка
1. Произвести магию по установке пакетов (пока что непонятно как, но мы стараемся это определить)

3. Создать файл `.env` со следующим содержимым
   ```bash
   CNC_SPREADSHEET_ID=ID_таблицы_в_google_sheets
   TELEGRAM_BOT_TOKEN=Тут_ваш_telegram_токен
   ```
4. Создать файл `token.json` в который требуется положить токен доступа к google-таблицам

### Запуск
```bash
python3 run.py
```

### Документация по библиотекам
- Telegram: [https://python-telegram-bot.readthedocs.io](https://python-telegram-bot.readthedocs.io)
- Google Sheets: [https://developers.google.com/docs/api/quickstart/python](https://developers.google.com/docs/api/quickstart/python)
- Loguru: [https://github.com/Delgan/loguru](https://github.com/Delgan/loguru)
