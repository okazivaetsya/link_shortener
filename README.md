![workflow status badge](https://github.com/okazivaetsya/link_shortener/actions/workflows/main.yml/badge.svg?event=push)  
# Сократитель ссылок
Сервис для сокращения ссылок реализованный в форме Web-приложение с API.  
Технологии: Django / DRF / Docker / NginX / Docker-compose / PostgreSQL / Unittest / GitHub Actions  

Разработка ведется с БД SQLite, а на сервере из Docker разворачиваем PostgreSQL&

## Входные данные
Проект выложен на http://158.160.26.117

Вход в админку:  
login: admin  
password: admin  

В админке можно посмотреть созданные токены и статистику переходов по ним.

## Описание
Сервис для сокращения ссылок работает через API. Для генерации короткой ссылки необходимо отправить POST-запрос в теле которого указать полную ссылку. После чего придет ответ со сгенерированным токеном (парой "полная ссылка - короткая ссылка"). Короткая ссылка представлена в виде последовательности из 6 символов содержащих цифры и большие и маленькие буквы латинского алфавита. Для того чтобы применить короткую ссылку необходимо вставить полученную последовательность символов сразу после знака вашего домена. Пример: https://my_domain.com/Tdh52Q  
В админке доступна функция деактивации ссылок, а также отображается статистика перехода по каждой ссылке.

## Программные требования
1) Сервер должен работать на ОС Linux (Ubuntu)
2) На сервере должен быть установлен Docker и docker-compose

## Установка
Установка приложения из контейнеров.
1) Склонируйте приложение из [репозитория](https://github.com/okazivaetsya/link_shortener.git)
2) Скопируйте на сервер два файла:
```bash
scp docker-compose.yml <user_name>@<ip>:/home/<user_name>/
scp nginx.conf <user_name>@<ip>:home/<user_name>/nginx/default.conf
```

3) Запустите docker-compose:
```bash
sudo docker-compose up -d --build
```

4) Выполните миграции:
```bash
sudo docker-compose exec web python3 manage.py migrate
```

5) Подгрузите статику:
```bash
sudo docker-compose exec web python3 manage.py collectstatic
```

6) Создайте суперпользователя:
```bash
sudo docker-compose exec web python3 manage.py createsuperuser
```

## Эндпоинты и примеры запросов
Для создания короткой ссылки необходимо отправить POST запрос на эндпоинт **/api/tokens**, в теле которого указать полную ссылку:
```bash
{
    "full_url": "https://testurl.com"
}
```
в ответ придет json с данными токена:
```bash
{
    "id": 1,
    "full_url": "https://testurl.com",
    "short_url": "5qiYuW",
    "requests_count": 0,
    "created_date": "2023-01-29T15:13:12.098414Z",
    "is_active": true
}
```
Итог: http://<ваш домен>/5qiYuW -> https://testurl.com

Приложение протестировано.

