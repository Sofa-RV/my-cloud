# My Cloud

Дипломный проект по профессии «Fullstack-разработчик на Python».

My Cloud — веб-приложение облачного хранилища файлов. Пользователь может зарегистрироваться, войти в систему, загружать файлы, изменять их имена и комментарии, скачивать, удалять файлы и формировать публичные ссылки.

Администратор может просматривать список пользователей, изменять признак администратора, удалять пользователей и работать с файловыми хранилищами любых пользователей.

## Возможности приложения

### Для обычного пользователя

- регистрация;
- вход и выход из системы;
- хранение состояния авторизации через Django-сессию;
- просмотр собственного файлового хранилища;
- загрузка файлов с комментарием;
- просмотр имени, размера и дат файла;
- скачивание файла;
- переименование файла;
- изменение комментария;
- удаление файла;
- создание публичной ссылки;
- скачивание файла по публичной ссылке.

### Для администратора приложения

- просмотр списка пользователей;
- просмотр полного имени и email пользователя;
- просмотр признака администратора;
- просмотр количества и размера файлов пользователя;
- изменение признака администратора;
- удаление пользователей;
- переход в хранилище выбранного пользователя;
- выполнение операций с файлами любого пользователя.

## Технологии

### Backend

- Python 3.10 или выше;
- Django;
- PostgreSQL;
- Django sessions;
- JSON API;
- Gunicorn для production-запуска;
- Nginx как reverse proxy при развёртывании на сервере.

### Frontend

- JavaScript;
- React;
- React Router;
- Redux;
- Webpack;
- Babel;
- Jest.

## Структура проекта

```text
my-cloud/
├── backend/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── frontend_dist/
│   │   ├── assets/
│   │   └── index.html
│   ├── media/
│   ├── static/
│   ├── storage/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates/
│   ├── .env
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   ├── dist/
│   ├── .babelrc
│   ├── jest.config.cjs
│   ├── package.json
│   ├── package-lock.json
│   └── webpack.config.js
├── .gitignore
└── README.md
```

Папки `.venv`, `node_modules`, `media`, frontend `dist` и файл `.env` не должны публиковаться в репозитории.

Production-сборка frontend, используемая Django, находится в:

```text
backend/frontend_dist/
```

## Требования

Перед установкой проекта необходимо установить:

- Python 3.10 или выше;
- Node.js 18 или выше;
- npm;
- PostgreSQL;
- Git.

Для production-развёртывания также понадобятся:

- Linux-сервер;
- SSH-доступ;
- Gunicorn;
- Nginx;
- домен или публичный IP-адрес;
- HTTPS-сертификат.

## Клонирование проекта

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd my-cloud
```

## Настройка PostgreSQL

Войдите в PostgreSQL под пользователем с правами администратора:

```bash
psql -U postgres
```

Создайте базу данных:

```sql
CREATE DATABASE my_cloud;
```

Создайте отдельного пользователя базы данных:

```sql
CREATE USER my_cloud_user WITH PASSWORD 'замените_на_пароль_базы';
```

Выдайте пользователю права:

```sql
ALTER ROLE my_cloud_user SET client_encoding TO 'utf8';
ALTER ROLE my_cloud_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE my_cloud_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE my_cloud TO my_cloud_user;
```

Для PostgreSQL 15 и выше дополнительно выполните:

```sql
\c my_cloud
GRANT ALL ON SCHEMA public TO my_cloud_user;
```

Выйдите из PostgreSQL:

```sql
\q
```

Не используйте в публичном README реальные пароли базы данных.

## Настройка backend

Перейдите в папку backend:

```bash
cd backend
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его в Git Bash:

```bash
source .venv/Scripts/activate
```

Для Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Для Linux:

```bash
source .venv/bin/activate
```

Обновите pip:

```bash
python -m pip install --upgrade pip
```

Установите Python-зависимости:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

В папке `backend` создайте файл:

```text
.env
```

Пример содержимого:

```env
DJANGO_SECRET_KEY=замените_на_случайный_секретный_ключ
DJANGO_DEBUG=True

POSTGRES_DB=my_cloud
POSTGRES_USER=my_cloud_user
POSTGRES_PASSWORD=замените_на_пароль_базы
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

MEDIA_ROOT=media
MAX_UPLOAD_SIZE_MB=100

DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Сгенерировать секретный ключ можно командой:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Полученное значение нужно указать в `DJANGO_SECRET_KEY`.

Файл `.env` нельзя добавлять в Git:

```bash
git check-ignore -v backend/.env
```

## Миграции базы данных

Из папки `backend` проверьте наличие миграций:

```bash
python manage.py makemigrations --check
```

Если команда завершилась без сообщений, незакоммиченных изменений моделей нет.

Примените миграции:

```bash
python manage.py migrate
```

В проекте используются миграции приложений:

```text
backend/accounts/migrations/
backend/storage/migrations/
```

Проверьте настройки Django:

```bash
python manage.py check
```

Проверьте используемую базу данных:

```bash
python manage.py shell -c "from django.db import connection; print(connection.vendor); print(connection.settings_dict['NAME'])"
```

Для этого проекта ожидается:

```text
postgresql
my_cloud
```

## Создание администратора

Создайте суперпользователя Django:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям в терминале.

После этого назначьте пользователю признак администратора приложения:

```bash
python manage.py shell
```

Выполните в Django shell:

```python
from accounts.models import User

user = User.objects.get(username="admin")
user.is_app_admin = True
user.is_staff = True
user.save(update_fields=["is_app_admin", "is_staff"])
```

Выйдите из shell:

```python
exit()
```

У пользователя должны быть:

```text
is_app_admin = True
is_staff = True
```

## Запуск backend

Из папки `backend` выполните:

```bash
python manage.py runserver 127.0.0.1:8000
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

API будет доступен по адресу:

```text
http://127.0.0.1:8000/api/
```

`runserver` предназначен для локальной разработки. Для production необходимо использовать Gunicorn или другой production WSGI/ASGI-сервер.

## Настройка frontend

Откройте второй терминал и перейдите в папку frontend:

```bash
cd frontend
```

Установите зависимости:

```bash
npm install
```

## Запуск frontend в режиме разработки

Для запуска webpack-dev-server:

```bash
npm start
```

Frontend в режиме разработки будет доступен по адресу:

```text
http://127.0.0.1:3000/
```

При необходимости frontend должен обращаться к работающему backend Django.

## Production-сборка frontend

Из папки `frontend` выполните:

```bash
npm run build
```

Webpack создаст production-сборку в:

```text
frontend/dist/
```

После сборки скопируйте её в папку, из которой Django отдаёт frontend:

### Git Bash

```bash
rm -rf ../backend/frontend_dist/*
cp -r dist/* ../backend/frontend_dist/
```

### Windows PowerShell

```powershell
Remove-Item ..\backend\frontend_dist\* -Recurse -Force
Copy-Item .\dist\* ..\backend\frontend_dist\ -Recurse -Force
```

Проверьте, что в папке есть:

```text
backend/frontend_dist/index.html
backend/frontend_dist/assets/
```

Если Webpack выводит предупреждения о размере bundle, но завершает сборку сообщением `compiled successfully`, production-сборка создана успешно.

## Основные frontend-маршруты

```text
/                         Главная страница
/login                    Страница входа
/register                 Страница регистрации
/storage                  Собственное хранилище пользователя
/admin                    Административная панель
/storage/admin/:userId    Хранилище выбранного пользователя
```

Например:

```text
/storage/admin/6
```

открывает хранилище пользователя с идентификатором `6`.

Маршрут `/storage/admin/:userId` доступен только администратору приложения.


## API аутентификации

```text
GET  /api/auth/csrf/
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

### Получение CSRF-токена

```text
GET /api/auth/csrf/
```

Используется frontend перед запросами, которые изменяют состояние.

### Регистрация

```text
POST /api/auth/register/
```

Регистрация выполняется с проверкой:

- логина;
- полного имени;
- email;
- пароля;
- уникальности логина;
- уникальности email.

### Вход

```text
POST /api/auth/login/
```

После успешного входа создаётся сессия пользователя.

### Выход

```text
POST /api/auth/logout/
```

После выхода защищённые API-запросы должны возвращать ошибку авторизации.

### Текущий пользователь

```text
GET /api/auth/me/
```

Возвращает данные авторизованного пользователя.

## API пользователей

Доступ к API пользователей имеет только администратор приложения.

```text
GET    /api/auth/users/
DELETE /api/auth/users/<id>/
PATCH  /api/auth/users/<id>/admin/
```

### Список пользователей

```text
GET /api/auth/users/
```

Возвращает:

- логин;
- полное имя;
- email;
- признак администратора;
- количество файлов;
- общий размер файлов;
- идентификатор пользователя.

### Удаление пользователя

```text
DELETE /api/auth/users/<id>/
```

Доступно только администратору.

### Изменение признака администратора

```text
PATCH /api/auth/users/<id>/admin/
```

Доступно только администратору.

## API файлов

```text
GET    /api/files/
GET    /api/files/?owner_id=<user_id>
POST   /api/files/upload/
PATCH  /api/files/<id>/
DELETE /api/files/<id>/
GET    /api/files/<id>/download/
GET    /api/files/public/<token>/
```

### Список файлов

Для обычного пользователя:

```text
GET /api/files/
```

Возвращает файлы только текущего пользователя.

Для администратора:

```text
GET /api/files/?owner_id=<user_id>
```

Возвращает файлы выбранного пользователя.

Обычный пользователь не может использовать параметр `owner_id` для просмотра чужого хранилища.

### Загрузка файла

```text
POST /api/files/upload/
```

Запрос отправляется в формате `multipart/form-data`.

Передаются:

```text
file
comment
```

Размер файла ограничивается переменной:

```env
MAX_UPLOAD_SIZE_MB=100
```

### Изменение файла

```text
PATCH /api/files/<id>/
```

Используется для:

- переименования файла;
- изменения комментария.

Пример JSON:

```json
{
  "original_name": "new-name.txt",
  "comment": "Новый комментарий"
}
```

### Удаление файла

```text
DELETE /api/files/<id>/
```

После успешного удаления сервер возвращает:

```text
204 No Content
```

### Скачивание авторизованным пользователем

```text
GET /api/files/<id>/download/
```

Проверяются:

- наличие авторизации;
- права пользователя на хранилище;
- существование файла.

При скачивании обновляется дата последнего скачивания.

### Публичная ссылка

```text
GET /api/files/public/<token>/
```

Публичная ссылка формируется на основе случайного токена.

Пример:

```text
/api/files/public/f9df1a2b-b9a5-4aca-a681-c67a2d9876cf/
```

Ссылка не содержит:

- имени пользователя;
- логина;
- идентификатора хранилища;
- оригинального имени файла;
- пути к файлу на диске.

Публичное скачивание не требует авторизации. При скачивании сервер использует оригинальное имя файла.

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

- соответствовать формату электронной почты;
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

## Хранение файлов

Файлы сохраняются в каталоге:

```text
backend/media/
```

Папка `media` не должна публиковаться в GitHub.

Для каждого файла в базе данных сохраняются:

- оригинальное имя;
- размер;
- дата загрузки;
- дата последнего скачивания;
- комментарий;
- путь к файлу;
- публичный токен;
- владелец файла.

Файлы сохраняются под уникальными системными именами и разделяются по пользователям. Это предотвращает конфликт одинаковых имён файлов у разных пользователей.

Базовый каталог файлов настраивается через:

```env
MEDIA_ROOT=media
```

Максимальный размер файла:

```env
MAX_UPLOAD_SIZE_MB=100
```

## Права доступа

- регистрация доступна неавторизованным пользователям;
- защищённые API требуют авторизации;
- обычный пользователь работает только со своим хранилищем;
- администратор работает со своим и чужими хранилищами;
- список пользователей доступен только администратору;
- удаление пользователя доступно только администратору;
- изменение признака администратора доступно только администратору;
- публичный файл доступен по специальному токену без авторизации;
- пользователь не может скачать, переименовать или удалить чужой закрытый файл.

Ошибки API возвращаются:

- через HTTP-статус;
- в формате JSON;
- с сообщением, описывающим причину ошибки.

## Логирование

Backend выводит события в консоль с датой, временем и уровнем сообщения.

Используются уровни:

- `DEBUG`;
- `INFO`;
- `WARNING`;
- `ERROR`.

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

Пример:

```text
2026-08-24 15:13:39 [INFO] storage.views:
Файл загружен owner=cockache filename=comment-test.docx size=12621
```

## Тестирование backend

Из папки `backend` выполните:

```bash
python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py test
```

На момент подготовки проекта backend-тесты:

```text
Ran 26 tests
OK
```

Backend-тесты проверяют:

- регистрацию;
- валидацию логина;
- валидацию email;
- валидацию пароля;
- вход;
- выход;
- проверку сессии;
- административные операции;
- права доступа;
- загрузку файлов;
- скачивание файлов;
- публичные ссылки;
- переименование;
- изменение комментария;
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

## Ручная проверка приложения

### Регистрация

1. Откройте `/register`.
2. Введите корректные данные.
3. Проверьте успешную регистрацию.
4. Проверьте сообщения для некорректных данных.

### Вход и выход

1. Откройте `/login`.
2. Введите логин и пароль.
3. Проверьте переход в приложение.
4. Выполните выход.
5. Проверьте, что защищённые страницы больше недоступны.

### Работа с файлами

1. Войдите обычным пользователем.
2. Откройте `/storage`.
3. Загрузите файл с комментарием.
4. Скачайте файл.
5. Переименуйте файл.
6. Измените комментарий.
7. Обновите страницу.
8. Проверьте сохранение изменений.
9. Удалите файл.

### Публичная ссылка

1. Загрузите файл.
2. Скопируйте публичную ссылку.
3. Откройте ссылку в режиме инкогнито.
4. Убедитесь, что файл скачивается без авторизации.
5. Проверьте, что в URL нет логина, имени пользователя или имени файла.
6. Проверьте, что скачанный файл получил оригинальное имя.

### Администратор

1. Войдите под администратором.
2. Откройте `/admin`.
3. Проверьте список пользователей.
4. Измените признак администратора.
5. Откройте хранилище пользователя по адресу:
   ```text
   /storage/admin/<user_id>
   ```
6. Проверьте работу с файлами выбранного пользователя.

## Проверка deployment-настроек

Из папки `backend` выполните:

```bash
python manage.py check --deploy
```

Для локальной разработки возможны предупреждения, связанные с отсутствием HTTPS:

```text
SECURE_HSTS_SECONDS
SECURE_SSL_REDIRECT
SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE
DEBUG
```

Перед production-развёртыванием необходимо:

- установить `DEBUG=False`;
- указать production-домен в `DJANGO_ALLOWED_HOSTS`;
- настроить `CSRF_TRUSTED_ORIGINS`;
- включить HTTPS;
- установить `SECURE_SSL_REDIRECT=True`;
- установить `SESSION_COOKIE_SECURE=True`;
- установить `CSRF_COOKIE_SECURE=True`;
- настроить HSTS после проверки HTTPS.

Пример production `.env`:

```env
DJANGO_SECRET_KEY=сгенерированный_уникальный_секрет
DJANGO_DEBUG=False

POSTGRES_DB=my_cloud
POSTGRES_USER=my_cloud_user
POSTGRES_PASSWORD=реальный_пароль_базы
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

DJANGO_ALLOWED_HOSTS=example.ru,www.example.ru
CSRF_TRUSTED_ORIGINS=https://example.ru,https://www.example.ru

MEDIA_ROOT=/var/www/my-cloud/media
MAX_UPLOAD_SIZE_MB=100

DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=3600
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Не публикуйте production `.env` в репозитории.

## Развёртывание на REG.RU

Для проекта рекомендуется VPS/VDS или облачный сервер с Linux и SSH-доступом.

Актуальные параметры тарифа и доступность учебного промокода необходимо уточнить у куратора дипломного проекта или в личном кабинете REG.RU.

Документация REG.RU по SSH:

https://help.reg.ru/support/hosting/dostupy-i-podklyucheniye-panel-upravleniya-ftp-ssh/rabota-po-ssh-na-virtualnom-hostinge

Документация REG.RU по облачным серверам:

https://reg.cloud/support/cloud/oblachnyye-servery/

### Подключение к серверу

Пример подключения:

```bash
ssh root@SERVER_IP
```

Вместо `SERVER_IP` укажите публичный IP-адрес сервера.

### Обновление пакетов

```bash
sudo apt update
sudo apt upgrade -y
```

### Установка системных пакетов

```bash
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    nginx \
    git
```

Node.js можно установить по официальной инструкции Node.js или через репозиторий, используемый на сервере.

### Создание пользователя приложения

```bash
sudo adduser --system --group --home /var/www/my-cloud mycloud
```

Создайте каталог проекта:

```bash
sudo mkdir -p /var/www/my-cloud
sudo chown -R mycloud:mycloud /var/www/my-cloud
```

Переключитесь на пользователя приложения:

```bash
sudo -u mycloud -H bash
cd /var/www/my-cloud
```

### Клонирование проекта

```bash
git clone <URL_РЕПОЗИТОРИЯ> .
```

### Настройка PostgreSQL на сервере

Переключитесь на пользователя PostgreSQL:

```bash
sudo -u postgres psql
```

Выполните:

```sql
CREATE DATABASE my_cloud;
CREATE USER my_cloud_user WITH PASSWORD 'замените_на_надёжный_пароль';
ALTER ROLE my_cloud_user SET client_encoding TO 'utf8';
ALTER ROLE my_cloud_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE my_cloud_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE my_cloud TO my_cloud_user;
\c my_cloud
GRANT ALL ON SCHEMA public TO my_cloud_user;
\q
```

### Установка backend

```bash
cd /var/www/my-cloud/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

Создайте production `.env`:

```bash
nano /var/www/my-cloud/backend/.env
```

Укажите production-значения из раздела выше.

### Установка frontend-зависимостей

```bash
cd /var/www/my-cloud/frontend
npm install
npm run build
```

Скопируйте production-сборку:

```bash
rm -rf ../backend/frontend_dist/*
cp -r dist/* ../backend/frontend_dist/
```

### Миграции и статические файлы

```bash
cd /var/www/my-cloud/backend
source .venv/bin/activate

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Если суперпользователь ещё не создан:

```bash
python manage.py createsuperuser
```

Затем назначьте `is_app_admin=True` через Django shell, как описано выше.

### Проверка Gunicorn

Из папки `backend` выполните:

```bash
source .venv/bin/activate
gunicorn --bind 127.0.0.1:8001 config.wsgi:application
```

Проверьте приложение локально на сервере:

```bash
curl http://127.0.0.1:8001/
```

Остановите Gunicorn сочетанием:

```text
Ctrl+C
```

### Systemd-сервис

Создайте файл:

```bash
sudo nano /etc/systemd/system/mycloud.service
```

Содержимое:

```ini
[Unit]
Description=My Cloud Django application
After=network.target postgresql.service

[Service]
User=mycloud
Group=mycloud
WorkingDirectory=/var/www/my-cloud/backend
EnvironmentFile=/var/www/my-cloud/backend/.env
ExecStart=/var/www/my-cloud/backend/.venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8001 \
    config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mycloud
sudo systemctl start mycloud
```

Проверьте статус:

```bash
sudo systemctl status mycloud
```

Логи:

```bash
sudo journalctl -u mycloud -f
```

### Настройка Nginx

Создайте конфигурацию:

```bash
sudo nano /etc/nginx/sites-available/mycloud
```

Пример:

```nginx
server {
    listen 80;
    server_name example.ru www.example.ru;

    client_max_body_size 100M;

    location /static/ {
        alias /var/www/my-cloud/backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/my-cloud/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/mycloud /etc/nginx/sites-enabled/mycloud
sudo nginx -t
sudo systemctl reload nginx
```

Вместо `example.ru` укажите фактический домен или согласуйте использование публичного IP-адреса с куратором.

### HTTPS

После настройки домена можно установить сертификат Let's Encrypt:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.ru -d www.example.ru
```

После включения HTTPS обновите production `.env`:

```env
DJANGO_DEBUG=False
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

Затем перезапустите приложение:

```bash
sudo systemctl restart mycloud
sudo systemctl reload nginx
```

Повторно выполните:

```bash
python manage.py check --deploy
```

## Обновление приложения

После публикации изменений:

```bash
cd /var/www/my-cloud
sudo -u mycloud git pull
```

Обновите backend:

```bash
cd backend
sudo -u mycloud /var/www/my-cloud/backend/.venv/bin/pip install -r /var/www/my-cloud/backend/requirements.txt
sudo -u mycloud backend/.venv/bin/python manage.py migrate
sudo -u mycloud backend/.venv/bin/python manage.py collectstatic --noinput
```

Обновите frontend:

```bash
cd ../frontend
sudo -u mycloud npm install
sudo -u mycloud npm run build
sudo -u mycloud rm -rf ../backend/frontend_dist/*
sudo -u mycloud cp -r dist/* ../backend/frontend_dist/
```

Перезапустите сервис:

```bash
sudo systemctl restart mycloud
sudo systemctl reload nginx
```

## Проверка перед сдачей

### Backend

```bash
cd backend
source .venv/bin/activate

python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py test
```

### Frontend

```bash
cd ../frontend

npm test
npm run build
```

### Git

Из корня проекта:

```bash
cd ..
git status
```

Убедитесь, что в Git не попали:

```text
backend/.env
backend/.venv/
backend/media/
frontend/node_modules/
frontend/dist/
```

Проверить игнорируемые файлы:

```bash
git status --ignored
```

Проверить изменения README:

```bash
git diff -- README.md
```

## Результаты локальной проверки

На момент подготовки дипломного проекта подтверждены:

- подключение к PostgreSQL;
- база данных `my_cloud`;
- применение миграций;
- отсутствие ошибок `python manage.py check`;
- 26 пройденных backend-тестов;
- регистрация;
- вход;
- выход;
- сессии;
- административные права;
- список пользователей;
- удаление пользователей;
- изменение признака администратора;
- загрузка файлов;
- скачивание файлов;
- удаление файлов;
- переименование файлов;
- изменение комментариев;
- сохранение комментариев после обновления и повторного входа;
- публичное скачивание;
- обезличенные UUID-ссылки;
- React SPA;
- администраторский доступ к чужому хранилищу;
- логирование событий сервера.

## Полезная документация

- Django deployment checklist:  
  https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

- Django migrations:  
  https://docs.djangoproject.com/en/6.1/topics/migrations/

- Django static files:  
  https://docs.djangoproject.com/en/6.1/howto/static-files/

- REG.RU: работа по SSH:  
  https://help.reg.ru/support/hosting/dostupy-i-podklyucheniye-panel-upravleniya-ftp-ssh/rabota-po-ssh-na-virtualnom-hostinge

- REG.RU: облачные серверы:  
  https://reg.cloud/support/cloud/oblachnyye-servery/

## Развёртывание

Приложение развёрнуто на VPS-сервере Ubuntu 22.04.

Адрес приложения:

http://194.58.102.223/storage

### Архитектура

```text
Браузер
  ↓
Nginx :80
  ↓
Gunicorn :8000
  ↓
Django REST API
  ↓
PostgreSQL
```

Frontend собран Webpack в production-режиме.

Backend запускается через Gunicorn и systemd-службу:

```text
my-cloud.service
```

## Тестирование

Функциональность проверена для администратора и обычного пользователя:

- вход в систему;
- отображение списка файлов;
- загрузка файла;
- скачивание файла;
- удаление файла;
- выход из аккаунта;
- повторный вход.

Все проверки завершились успешно для обеих ролей.

## Резервное копирование

Созданы резервные копии:

- backend и frontend;
- пользовательских файлов `media`;
- базы данных PostgreSQL;
- глобальных объектов PostgreSQL.

Резервные копии перенесены с VPS на локальный компьютер и проверены по контрольным суммам SHA-256. Все файлы прошли проверку с результатом `OK`.
