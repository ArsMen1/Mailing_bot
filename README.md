# SHP Mailing Bot

Telegram-бот для рассылки сообщений преподавателям Московской Школы Программистов.

### Функциональность
- Получение списка сообщений и адресатов из google-таблицы
- Batch-отправка их по адресатам.

### Технологический стек
- python-telegram-bot
- google-api-python-client

### Первичная настройка
1. Создать файл `.env` со следующим содержимым
   ```bash
   CNC_SPREADSHEET_ID=ID_таблицы_в_google_sheets
   TELEGRAM_BOT_TOKEN=Тут_ваш_telegram_токен
   ```
2. Создать файл `token.json` в который требуется положить токен доступа к google-таблицам

3. Сделать Makefile исполняемым
   ```bash
   chmod +x Makefile
   ```   
 
4. Создать образ  
    ```bash
    docker build -t mailing_bot .
    ```


### Запуск контейнера
```bash
./Makefile
```

### Остановка 
1. Смотрим id запущенного контейнера
```bash
docker ps
```

2. Останавливаем нужный процесс 
```bash
docker stop <container id>
```


### Документация по библиотекам
- Telegram: [https://python-telegram-bot.readthedocs.io](https://python-telegram-bot.readthedocs.io)
- Google Sheets: [https://developers.google.com/docs/api/quickstart/python](https://developers.google.com/docs/api/quickstart/python)
- Loguru: [https://github.com/Delgan/loguru](https://github.com/Delgan/loguru)

