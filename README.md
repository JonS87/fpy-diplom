# Cloud Storage Web Application

## Описание

Это веб-приложение работает как облачное хранилище, позволяя пользователям загружать, скачивать, управлять и отправлять файлы. Приложение построено с использованием Django на бэкенде и React на фронтенде.

## Технологии

- **Бэкенд**: Python, Django, PostgreSQL
- **Фронтенд**: JavaScript, React, Redux, React Router
- **Инструменты**: Git, Node.js, Webpack

## Установка и запуск
### 1. Установка необходимых пакетов
Убедитесь, что на вашем сервере установлены необходимые пакеты:
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl python3-venv
```
### 2. Клонирование репозитория
Сначала клонируйте репозиторий на свой удаленный сервер:
```bash
git clone https://github.com/JonS87/fpy-diplom.git
cd fpy-diplom
```

### 3. Установка бэкенда
#### 3.1. Создание виртуального окружения
Создайте и активируйте виртуальное окружение:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
```
#### 3.2. Установка зависимостей
Установите необходимые зависимости для Django:
```bash
pip install -r requirements.txt
pip install packaging typing_extensions
```
#### 3.3. Настройка базы данных
Убедитесь, что PostgreSQL установлен и запущен.
Создайте базу данных для приложения:
```sql
CREATE DATABASE mycloud WITH ENCODING 'UTF8';
```
### 3.4. Создание и настройка файла .env
#### 3.4.1 Создайте файл .env
В терминале, в корневом каталоге серверной части проекта, выполните команду:
```bash
touch .env
```
#### 3.4.2. Откройте файл .env в текстовом редакторе:
Например, с помощью nano:
```bash
nano .env
```
#### 3.4.3. Наполните файл .env необходимыми переменными:
Добавьте следующие строки, заполнив значениями переменные:
```plaintext
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
CORS_ALLOWED_ORIGINS=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DJANGO_LOG_LEVEL=
```
#### 3.4.4. Сохраните и закройте файл:
Если вы используете nano, нажмите CTRL + X, затем Y, и затем ENTER для сохранения изменений.
#### 3.5. Применение миграций
Примените миграции для инициализации базы данных:
```bash
python manage.py migrate
```
#### 3.6. Создание суперпользователя
Создайте суперпользователя для доступа к административному интерфейсу:
```bash
python manage.py createsuperuser
```
### 4. Установка и настройка Gunicorn
Установите Gunicorn:
```bash
pip install gunicorn
```
Настройка Gunicorn:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Добавьте следующую конфигурацию:
```bash
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/evgeniy/fpy-diplom/backend
ExecStart=/home/evgeniy/fpy-diplom/backend/venv/bin/gunicorn --access-logfile -\
          --workers=3 \
          --bind unix:/home/evgeniy/fpy-diplom/backend/main/project.sock main.wsgi:application

[Install]
WantedBy=multi-user.target
```
Убедитесь что пользователь www-data имеет права на чтение и запись в директорию /home/evgeniy/fpy-diplom/backend.
Запустите Gunicorn для вашего приложения:
```bash
sudo systemctl start gunicorn
```
Чтобы Gunicorn автоматически запускался при загрузке системы, выполните:
```bash
sudo systemctl enable gunicorn
```
Для проверки статуса службы выполните:
```bash
sudo systemctl status gunicorn
```
### 5. Запуск бэкенда
Запустите сервер Django:
```bash
python manage.py runserver
```
### 6. Установка фронтенда
#### 6.1. Переход в директорию фронтенда
Откройте вторую IDE и перейдите в директорию фронтенда:
```bash
cd ..
cd frontend
```
#### 6.2. Установка зависимостей
Установите необходимые зависимости для React:
```bash
npm install
```
### 6.3 Создание и настройка файла .env
#### 6.3.1 Создайте файл .env
В терминале, в корневом каталоге серверной части проекта, выполните команду:
```bash
touch .env
```
#### 6.3.2. Откройте файл .env в текстовом редакторе:
Например, с помощью nano:
```bash
nano .env
```
#### 6.3.3. Наполните файл .env необходимыми переменными:
Добавьте следующие строки, заполнив значениями переменные:
```ini
VITE_API_URL=http://127.0.0.1:8000/api/
```
#### 6.4. Запуск фронтенда
Запустите приложение React:
```bash
npm run build
```
#### 7. Настройка Nginx
Создайте новый файл конфигурации для вашего приложения:
```bash
sudo nano /etc/nginx/sites-available/mycloud
```
Добавьте следующую конфигурацию:
```nginx
server{
        listen 443 ssl;
        server_name 193.227.240.10;
        server_tokens off;

        ssl_certificate /home/evgeniy/fpy-diplom/backend/mycert.crt;
        ssl_certificate_key /home/evgeniy/fpy-diplom/backend/mykey.key;

        # Настройка для фронтенда
        location / {
                root /home/evgeniy/fpy-diplom/frontend/dist;
                index index.html index.htm;
                try_files $uri $uri/ /index.html;  # Для SPA
        }

        location /static/ {
                root /home/evgeniy/fpy-diplom/backend;
        }

        location /media/ {
                alias /home/evgeniy/fpy-diplom/backend/media/;
                # autoindex on;
        }

        location /api {
                include proxy_params;
                proxy_pass http://unix:/home/evgeniy/fpy-diplom/backend/main/pr>
        }

        location /admin {
                include proxy_params;
                proxy_pass http://unix:/home/evgeniy/fpy-diplom/backend/main/pr>
        }
}
```
Настройка конфигурационного файла Nginx:
```bash
sudo nano /etc/nginx/nginx.conf
```
Добавьте следующую конфигурацию:
```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
         error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss tex>

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;

        client_max_body_size 15M;
}
```

Активируйте конфигурацию и перезапустите Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/mycloud /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
### 8. Доступ к приложению
После запуска серверов, вы сможете получить доступ к приложению по адресу:
- **Фронтенд**: [http://<ваш_адрес_сервера>/](http://<ваш_адрес_сервера>/)
- **Административный интерфейс Django**: [http://<ваш_адрес_сервера>/admin](http://<ваш_адрес_сервера>/admin)
## Использование
1. Перейдите на главную страницу приложения.
2. Зарегистрируйтесь или войдите в систему.
3. Используйте интерфейс для загрузки, скачивания и управления файлами.
## Лицензия
Этот проект лицензирован под MIT License - подробности смотрите в файле [LICENSE](LICENSE).
## Контакты
Если у вас есть вопросы, вы можете связаться со мной по электронной почте: evgeniy@chausov.ru.

### Примечания:
- Замените `<ваш_адрес_сервера>` на фактический адрес вашего сервера.
- Убедитесь, что вы настроили пути для статических и медиафайлов в конфигурации Nginx.
- Проверьте, что все команды выполняются с необходимыми правами (например, с использованием `sudo`, если это требуется).
