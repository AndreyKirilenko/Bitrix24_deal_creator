# test_2

Тестовое задание. Написать программу(скрипт) на языке Python, которая будет создавать задачи в системе Bitrix24 за три дня до наступления государственных праздников.

## Локальная установка. 
Для установки: 
* скачайте проект к себе на компьютер 
```bash
    git clone <url repo>
```
* Установите Docker 
```bash
    https://www.docker.com/get-started
```
* установите виртуальное окружение
```bash
    py -m venv venv
```
* Активируйте виртуальное окружение
```bash
    source venv/Scripts/activate
```
* Выполните миграции
```bash
    py manage.py makemigrations
    py manage.py migrate
```
* создайте в корне рядом с Dockerfile, файл ```.env``` с переменными окружения
```python
    WEBHOOK=<ваш вебхук> # Ваш вебхук из личного кабинета Bitrix24
```
* В корне проекта запустите создание Docker образа
```bash
    docker build -t test .
```

* Запустите контейнер из образа
```bash
    docker run --name test -it test
```


## Эндпойнты 

Эндпойнт создает пользовательские поля в сущинсти сделка srm.dea
```python
GET http://127.0.0.1:8000/create_userfield/
Content-Type: application/json
```
```python
    "DESCRIPTION"
    "DELIVERY_ADRESS"
    "DELIVERY_DATE"
    "DELIVERY_CODE"
```

после создания пользовательских полей можно использовать основной
```python
    POST http://127.0.0.1:8000/
    Content-Type: application/json

    {
        "title": "Тестовая сделка",
        "description": "Some description",
        "client": {
            "name": "Jonnyw",
            "surname": "Karter",
            "phone": "823551444432",
            "adress": "st. Mira, 287, Moscow"
        },
        "products": ["Candy", "Carrot", "Potato"],
        "delivery_adress": "st. Mira, 211, Ekaterinburgg",
        "delivery_date": "2021-01-01:16:00",
        "delivery_code": "#232nkF155wwwwn"
    }
```
* Приложение принимает заявку в JSON, после валидации
* Проверяет наличие указанного в заявке контакта в Bitrix24, если нет, создает контакт
и сделку для этого контакта
* Если контакт есть, проверяет есть ли указанная сделка по delivery_code,
    * если сделки нет - создает новую сделку для этого контакта
    * если сделка есть - сравнивает ее с новой и при нахождении отличий обновляет данные


При разработке использовался фреймворк Django и API фреймвок djangorestframework. 
Для отправки запросов к Bitrix24 использована библиотека fast-bitrix24
Для хранения переменных среды и обеспечения секретности вебхуков использовалась библиотека python-dotenv

технологии:
- django
- djangorestframework
- fast-bitrix24
- python-dotenv


