# MLService

## Доступные команды
- `./manage.py flask run [--host 0.0.0.0]` - запуск сервера flask на стандартном порте 5000

- `./manage.py compose [up, down] [-d]` - запуск и остановка docker контейнеров. По умолчанию запускается development контейнер

- `./manage.py compose [build] [name]` - создание соответствующего docker образа

- `./manage.py create-initial-db` - инициализация БД.

- `./manage.py migrate [--revision] [--autogenerate] [-m] [name]` - создание файлов миграции БД.

- `./manage.py migrate [upgrade] [head]` - миграция БД.

- `./manage.py test` - запуск тестов.
