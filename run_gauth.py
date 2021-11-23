from google_auth import authorize

# Используется только один раз для получения файла token.json. Не работает из-за относительности путей.
if __name__ == '__main__':
    authorize()
