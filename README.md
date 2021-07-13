# [Foodgram-project](http://84.201.179.82/)

## Проект Foodgram-project - "Продуктовый помощник".

Это сайт, который позволяет посетителям просматривать опубликованные рецепты кулинарных блюд, а зарегистрированным пользователям публиковать, добавлять в избранное понравившиеся рецепты, а так же составлять и скачивать список ингредиентов понравившихся блюд.

## Стек

- Python
- Django
- Postgresql
- Nginx
- Docker

## Установка на сервер Linux w/Docker

1. Установите [проект](https://ibb.co/ynK46Wq) на сервер.

2. Перейдите в директорию проекта и создайте файл '.env' :

```
   DB_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   SECRET_KEY=<ваш ключ>
```

SECRET_KEY можно сгенерировать по [ссылке](http://djecrety.ir/)

 3. В директории проекта выполните

    ```
    - docker-compose up #собираем и запускаем контейнеры проекта в docker
    - docker-compose exec web python manage.py migrate #выполняем миграции
    - docker-compose exec web python manage.py collectstatic #собираем статику
    - docker-compose exec web python manage.py createsuperuser #создаем суперпользователя
    ```

<!-- Пример работы проекта можно увидеть [по этому адресу](http://84.201.179.82/) -->

