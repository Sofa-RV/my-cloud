# My Cloud

Облачное хранилище My Cloud — дипломный fullstack-проект по профессии «Fullstack-разработчик на Python».

Приложение позволяет пользователям:

- регистрироваться и входить в систему;
- загружать файлы;
- просматривать список файлов;
- скачивать файлы;
- переименовывать файлы;
- изменять комментарии;
- удалять файлы;
- создавать публичные ссылки;
- скачивать файлы по публичной ссылке.

Администратор дополнительно может:

- просматривать список пользователей;
- видеть количество и общий размер файлов пользователей;
- изменять признак администратора;
- удалять пользователей;
- открывать хранилище выбранного пользователя;
- управлять файлами выбранного пользователя.

## Технологии

### Backend

- Python 3.10 или новее;
- Django 5.1.6;
- Django REST Framework 3.17.1;
- PostgreSQL;
- psycopg2-binary;
- django-cors-headers;
- python-dotenv;
- сессионная аутентификация;
- Django ORM;
- REST API;
- логирование в консоль.

### Frontend

- JavaScript;
- React 18.3.1;
- Redux Toolkit 2.8.2;
- React Redux 9.2.0;
- React Router DOM 6.30.1;
- Axios 1.11.0;
- Webpack 5.101.3;
- Jest;
- React Testing Library.

## Структура проекта

```text
my-cloud/
├── backend/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── storage/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── store/
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.js
│   │   │   │   └── filesSlice.js
│   │   │   └── store.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.test.jsx
│   │   ├── index.jsx
│   │   ├── setupTests.js
│   │   ├── styles.css
│   │   └── testStyleMock.js
│   ├── .babelrc
│   ├── jest.config.cjs
│   ├── package.json
│   ├── package-lock.json
│   └── webpack.config.js
├── .gitignore
└── README.md
```

## Требования

Перед запуском необходимо установить:

- Python версии 3.10 или новее;
- PostgreSQL;
- Node.js версии 18 или новее;
- npm;
- Git.

## Настройка PostgreSQL

Перед запуском приложения необходимо создать базу данных и пользователя PostgreSQL.

Выполните следующие SQL-команды:

```sql
CREATE DATABASE my_cloud;

CREATE USER my_cloud_user
WITH PASSWORD 'my_cloud_password';

ALTER ROLE my_cloud_user
SET client_encoding TO 'utf8';

ALTER ROLE my_cloud_user
SET default_transaction_isolation
TO 'read committed';

ALTER ROLE my_cloud_user
SET timezone TO 'Europe/Moscow';

GRANT ALL PRIVILEGES
ON DATABASE my_cloud
TO my_cloud_user;
```

Для PostgreSQL 15 и новее дополнительно выполните:

```sql
\c my_cloud

GRANT ALL
ON SCHEMA public
TO my_cloud_user;

GRANT ALL PRIVILEGES
ON ALL TABLES
IN SCHEMA public
TO my_cloud_user;

GRANT ALL PRIVILEGES
ON ALL SEQUENCES
IN SCHEMA public
TO my_cloud_user;
```

## Настройка backend

Перейдите в папку backend:

```bash
cd backend
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте виртуальное окружение.

Для Git Bash:

```bash
source .venv/Scripts/activate
```

Для Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Для Windows CMD:

```cmd
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

Перед запуском необходимо создать файл:

```text
backend/.env
```

Добавьте в него следующие значения:

```env
DJANGO_SECRET_KEY=замените_на_свой_секретный_ключ
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=my_cloud
POSTGRES_USER=my_cloud_user
POSTGRES_PASSWORD=my_cloud_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

PUBLIC_FILE_BASE_URL=http://127.0.0.1:8000/api/files/public
MAX_UPLOAD_SIZE_MB=100

DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Файл `backend/.env` нельзя публиковать в репозитории.

Для генерации секретного ключа выполните:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Полученное значение укажите вместо:

```env
замените_на_свой_секретный_ключ
```

## Выполнение миграций

Перед первым запуском необходимо проверить состояние миграций:

```bash
python manage.py makemigrations --check
```

Примените миграции:

```bash
python manage.py migrate
```

Проверьте настройки Django:

```bash
python manage.py check
```

## Создание администратора

Для создания пользователя администратора Django выполните:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям в терминале.

После создания пользователя установите ему признак администратора приложения.

Запустите Django shell:

```bash
python manage.py shell
```

Выполните:

```python
from accounts.models import User

user = User.objects.get(
    username="admin",
)

user.is_app_admin = True

user.save(
    update_fields=[
        "is_app_admin",
    ],
)
```

Завершите работу shell:

```python
exit()
```

## Запуск backend

Из папки `backend` выполните:

```bash
python manage.py runserver 127.0.0.1:8000
```

Backend API будет доступен по адресу:

```text
http://127.0.0.1:8000/api/
```

## Настройка frontend

Откройте второй терминал и перейдите в папку frontend:

```bash
cd frontend
```

Установите зависимости:

```bash
npm install
```

## Запуск frontend

Для запуска frontend в режиме разработки выполните:

```bash
npm start
```

Frontend будет доступен по адресу:

```text
http://127.0.0.1:3000/
```

## Production-сборка frontend

Для создания production-сборки выполните:

```bash
npm run build
```

Собранные файлы будут созданы в папке:

```text
frontend/dist/
```

Если Webpack выводит предупреждения о размере bundle, но завершает работу сообщением:

```text
compiled successfully
```

сборка выполнена успешно.

## Тестирование backend

Из папки `backend` выполните:

```bash
python manage.py test
```

Backend-тесты проверяют:

- регистрацию пользователя;
- валидацию логина;
- валидацию email;
- валидацию пароля;
- вход пользователя;
- выход пользователя;
- проверку сессии;
- административные операции;
- права доступа;
- загрузку файлов;
- скачивание файлов;
- публичные ссылки;
- переименование файлов;
- изменение комментариев;
- удаление файлов;
- ограничение размера файлов.

## Тестирование frontend

Из папки `frontend` выполните:

```bash
npm test
```

Frontend-тесты проверяют:

- отображение формы входа;
- отображение главной страницы;
- переход к регистрации;
- проверку несовпадающих паролей;
- успешный вход;
- отображение пользовательской панели;
- работу React Router в тестовой среде.

## Основные маршруты frontend

```text
/                       Главная страница
/login                  Страница входа
/register               Страница регистрации
/storage                Собственное файловое хранилище
/admin                  Административная панель
/admin/storage/:userId  Хранилище выбранного пользователя
```

Маршрут:

```text
/admin/storage/:userId
```

доступен только пользователю с признаком администратора.

Например:

```text
/admin/storage/5
```

открывает хранилище пользователя с идентификатором `5`.

## API аутентификации

```text
GET  /api/auth/csrf/
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

## API пользователей

```text
GET    /api/auth/users/
DELETE /api/auth/users/<id>/
PATCH  /api/auth/users/<id>/admin/
```

## API файлов

```text
GET    /api/files/
POST   /api/files/upload/
PATCH  /api/files/<id>/
DELETE /api/files/<id>/
GET    /api/files/<id>/download/
GET    /api/files/public/<token>/
```

Для администратора доступен запрос файлов выбранного пользователя:

```text
GET /api/files/?owner_id=<user_id>
```

Обычный пользователь получает только файлы собственного хранилища.

## Ограничения регистрации

### Логин

Логин должен:

- содержать от 4 до 20 символов;
- начинаться с латинской буквы;
- содержать только латинские буквы и цифры;
- быть уникальным.

Корректный пример:

```text
Sonya2026
```

Некорректные примеры:

```text
123sonya
so
sonya-user
соня
```

### Полное имя

Полное имя не должно быть пустым.

### Email

Email должен:

- соответствовать формату email;
- быть уникальным;
- не содержать лишних пробелов.

### Пароль

Пароль должен:

- содержать не менее 6 символов;
- содержать хотя бы одну заглавную букву;
- содержать хотя бы одну цифру;
- содержать хотя бы один специальный символ.

Корректный пример:

```text
MyCloud1!
```

## Работа с файлами

Пользователь может:

- загрузить новый файл;
- добавить комментарий;
- просмотреть список файлов;
- увидеть размер файла;
- увидеть дату загрузки;
- увидеть дату последнего скачивания;
- скачать файл;
- переименовать файл;
- изменить комментарий;
- удалить файл;
- скопировать публичную ссылку.

Администратор может выполнять эти операции со своим хранилищем и хранилищами других пользователей.

## Хранение файлов

Загруженные файлы сохраняются в каталоге:

```text
backend/media/
```

В базе данных сохраняется:

- оригинальное имя файла;
- размер;
- дата загрузки;
- дата последнего скачивания;
- комментарий;
- путь к файлу;
- публичный токен.

Файлы хранятся под уникальными системными именами и разделяются по пользователям, чтобы одинаковые имена файлов не конфликтовали.

Максимальный размер файла задаётся переменной:

```env
MAX_UPLOAD_SIZE_MB=100
```

## Публичные ссылки

Публичная ссылка формируется с использованием специального токена:

```text
/api/files/public/<token>/
```

Ссылка не содержит:

- логин пользователя;
- имя каталога пользователя;
- оригинальное имя файла.

При скачивании сервер использует оригинальное имя файла.

## Права доступа

- неавторизованный пользователь не имеет доступа к защищённым API;
- обычный пользователь работает только со своим хранилищем;
- администратор может работать с хранилищами любых пользователей;
- удаление пользователей доступно только администратору;
- изменение признака администратора доступно только администратору;
- публичный файл доступен по специальному токену без авторизации.

## Логирование

Backend выводит сообщения в консоль.

Логируются:

- регистрация;
- вход;
- выход;
- загрузка файла;
- скачивание файла;
- удаление файла;
- административные изменения;
- запрещённые запросы;
- ошибки API.

Пример сообщения:

```text
2026-08-19 22:01:42 [INFO] storage.views:
Файл загружен owner=testuser filename=test.txt size=17
```

## Проверка перед фиксацией изменений

Из корневой папки проекта выполните:

```bash
git status
```

Проверьте, что в список изменений не попали:

```text
backend/.env
backend/media/
backend/staticfiles/
frontend/node_modules/
```

Проверьте backend:

```bash
cd backend
python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py test
```

Проверьте frontend:

```bash
cd ../frontend
npm test
npm run build
```

Вернитесь в корень проекта:

```bash
cd ..
git status
```

## Подготовка к production

Перед развёртыванием необходимо:

- создать production PostgreSQL;
- установить зависимости backend;
- создать production `.env`;
- установить Gunicorn;
- выполнить миграции;
- собрать статические файлы;
- настроить Nginx;
- настроить HTTPS;
- указать production-домен в `ALLOWED_HOSTS`;
- выполнить deployment-проверку Django.

Django рекомендует запускать deployment-проверку командой:

```bash
python manage.py check --deploy
```

Команда должна выполняться с production-настройками. [757]

Для production-переменных окружения используются значения:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.ru,www.example.ru

DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=3600
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

## Развёртывание на REG.RU

Финальное приложение должно быть развёрнуто на платформе REG.RU.

Для проекта рекомендуется использовать VPS или облачный сервер с Linux.

Рекомендуемая схема:

```text
REG.RU VPS
├── Nginx
├── Gunicorn
├── Django
├── PostgreSQL
├── frontend/dist
├── staticfiles
└── media
```

Установка системных пакетов на Ubuntu:

```bash
sudo apt update

sudo apt install \
  python3 \
  python3-venv \
  python3-pip \
  postgresql \
  nginx \
  git
```

Клонирование проекта:

```bash
git clone <URL_РЕПОЗИТОРИЯ> /var/www/my-cloud

cd /var/www/my-cloud/backend
```

Создание виртуального окружения:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Установка Python-зависимостей:

```bash
pip install -r requirements.txt
```

Установка Gunicorn:

```bash
pip install gunicorn
```

Создание production-файла окружения:

```text
/var/www/my-cloud/backend/.env
```

Пример production `.env`:

```env
DJANGO_SECRET_KEY=production_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.ru,www.example.ru

POSTGRES_DB=my_cloud
POSTGRES_USER=my_cloud_user
POSTGRES_PASSWORD=production_database_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

PUBLIC_FILE_BASE_URL=https://example.ru/api/files/public
MAX_UPLOAD_SIZE_MB=100

DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=3600
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Применение миграций:

```bash
python manage.py migrate
```

Сбор статических файлов:

```bash
python manage.py collectstatic --noinput
```

Проверка production-настроек:

```bash
python manage.py check --deploy
```

Проверка запуска Gunicorn:

```bash
gunicorn \
  --bind 127.0.0.1:8000 \
  config.wsgi:application
```

Для постоянной работы приложения необходимо настроить systemd-сервис Gunicorn.

Nginx используется как reverse proxy перед Gunicorn. Конкретные значения домена, IP-адреса, имени базы данных и пользователя зависят от выбранной конфигурации REG.RU.

## Безопасность

Нельзя публиковать:

```text
backend/.env
backend/media/
backend/staticfiles/
frontend/node_modules/
frontend/dist/
```

Перед публикацией необходимо выполнить:

```bash
git status
```

В выводе не должно быть:

```text
backend/.env
```

Секретный ключ, пароль PostgreSQL и production-настройки должны храниться только в переменных окружения.

## Финальная проверка

Backend:

```bash
cd backend

python manage.py check
python manage.py makemigrations --check
python manage.py migrate
python manage.py test
```

Frontend:

```bash
cd ../frontend

npm test
npm run build
```

Git:

```bash
cd ..

git status
git log --oneline
```

Production:

```bash
cd backend

python manage.py check --deploy
```

## Лицензия

Проект создан в учебных целях в рамках дипломной работы по профессии «Fullstack-разработчик на Python».