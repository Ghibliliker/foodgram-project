[![foodgram-workflow](https://github.com/Ghibliliker/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Ghibliliker/foodgram-project-react/actions/workflows/main.yml)
 
#  Дипломный проект курса Python-разработчик Яндекс-Практикум

###  О чем проект:

Сервис Foodgram - продуктовый помощник, пользователь может публиковать свои рецепты, подписываться на других пользователей, проводить фильтрацию по тегам, возможно добавление рецептов в "Избранное" и скачивать список необходимых ингредиентов для выбранных рецептов

### Ссылка на проект:

62.84.126.99

для ревью:
123qwert@yandex.com
klm854po91

### Стек технологий
```
Python 3
Django
Django REST Framework
Djoser
Docker
```

## Как запустить проект:
 
 1. Скачать проект
 2. Установить docker, docker-compose
 3. Создать .env с нижепредставленными переменными
 ```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=SECRET_KEY (секретный ключ Django)
```
4. Сборка и запуск контейнера docker-compose up -d --build
5. Миграции docker-compose exec backend python manage.py makemigrations docker-compose exec backend python manage.py migrate
6. Сбор статики docker-compose exec backend python manage.py collectstatic --noinput
7. Создание суперпользователя Django docker-compose exec backend python manage.py createsuperuser

Документация проекта:
62.84.126.99/api/docs/

Автор проекта: Pavel Maslo
