### Hexlet tests and linter status:
[![Actions Status](https://github.com/BRODER1CK/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/BRODER1CK/python-project-83/actions) <a href="https://codeclimate.com/github/BRODER1CK/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/378427d63fd8f26bf2e8/maintainability" /></a>

# Анализатор страниц

Page Analyzer — полноценное приложение, основанное на фреймворке Flask. Это сайт, который анализирует определенные страницы на предмет пригодности для SEO.

# Требования к установке

`python ^3.8`

`gunicorn ^20.1.0`

`flask ^2.2.2`

`python-dotenv ^0.21.0`

`psycopg2-binary ^2.9.5`

`validators ^0.20.0`

`requests ^2.28.1`

`beautifulsoup4 ^4.11.1`

# Инструкция по установке

1. `git clone https://github.com/BRODER1CK/python-project-83`

2. `cd python-project-83`

3. Убедитесь, что у Вас установлен PostgreSQL. Введите команду (большими буквами написан пример, вставляете свое название) - `createdb ВАША_БАЗА_ДАННЫХ`

4. `psql ВАША_БАЗА_ДАННЫХ`

После чего открывается консоль управления базой данных. Вам нужно зайти в файл database.sql в директории, скопировать оттуда все и вставить в консоль.

5. Создаем в директории файл с названием ".env". Добавляем туда переменные окружения (большими буквами написаны примеры, вставляете свои данные):

`DATABASE_URL = postgresql://ВАШ_ЛОГИН:ВАШ_ПАРОЛЬ@localhost:5432/ВАША_БАЗА_ДАННЫХ`

`SECRET_KEY = 'ВАШ_СЕКРЕТНЫЙ_КЛЮЧ'`

6. `poetry install`

# Описание работы

Запустите сервер Flask Gunicorn, выполнив команду - `make start`

По умолчанию сервер будет доступен по адресу `http://0.0.0.0:8000`

Также возможно запустить его локально в режиме разработки с активным отладчиком, используя команду - `make dev`

Сервер разработки будет находиться по адресу `http://127.0.0.1:5000`

Чтобы добавить новый сайт, введите его адрес в форму на главной странице. Указанный адрес будет проверен и затем добавлен в базу данных.

После того, как сайт добавлен, вы можете приступить к его проверке. На странице конкретного сайта появляется кнопка, и нажатие на нее создает запись в таблице проверки.

Вы можете увидеть все добавленные URL-адреса на странице /urls.

# Попробовать проект в работе вы можете [ЗДЕСЬ](https://python-project-83-production-3071.up.railway.app/)  