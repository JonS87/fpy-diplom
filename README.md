# Cloud Storage Web Application

## Описание

Это веб-приложение работает как облачное хранилище, позволяя пользователям загружать, скачивать, управлять и отправлять файлы. Приложение построено с использованием Django на бэкенде и React на фронтенде.

## Технологии

- **Бэкенд**: Python, Django, PostgreSQL
- **Фронтенд**: JavaScript, React, Redux, React Router
- **Инструменты**: Git, Node.js, Webpack

## Установка и запуск
### 1. Клонирование репозитория
Сначала клонируйте репозиторий на свою локальную машину:
```bash
git clone https://github.com/JonS87/fpy-diplom.git
cd fpy-diplom
```

### 2. Установка бэкенда
#### 2.1. Создание виртуального окружения
Создайте и активируйте виртуальное окружение:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
```
#### 2.2. Установка зависимостей
Установите необходимые зависимости для Django:
```bash
pip install -r requirements.txt
```
#### 2.3. Настройка базы данных
Убедитесь, что PostgreSQL установлен и запущен.
Создайте базу данных для приложения:
```sql
CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
```
### Примечания
- Замените `your_database_name`, `your_username` и `your_password` на соответствующие значения.
### 2.4. Создание и настройка файла .env
#### 2.4.1 Создайте файл .env
В терминале, в корневом каталоге серверной части проекта, выполните команду:
```bash
touch .env
```
#### 2.4.2. Откройте файл .env в текстовом редакторе:
Например, с помощью nano:
```bash
nano .env
```
#### 2.4.3. Наполните файл .env необходимыми переменными:
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
#### 2.4.4. Сохраните и закройте файл:
Если вы используете nano, нажмите CTRL + X, затем Y, и затем ENTER для сохранения изменений.
#### 2.5. Применение миграций
Примените миграции для инициализации базы данных:
```bash
python manage.py migrate
```
#### 2.6. Создание суперпользователя
Создайте суперпользователя для доступа к административному интерфейсу:
```bash
python manage.py createsuperuser
```
### 3. Запуск бэкенда
Запустите сервер Django:
```bash
python manage.py runserver
```
### 4. Установка фронтенда
#### 4.1. Переход в директорию фронтенда
Перейдите в директорию фронтенда:
```bash
cd ..
cd frontend
```
#### 4.2. Установка зависимостей
Установите необходимые зависимости для React:
```bash
npm install
```
#### 4.3. Запуск фронтенда
Запустите приложение React:
```bash
npm run dev
```
### 5. Доступ к приложению
После запуска серверов, вы сможете получить доступ к приложению по адресу:
- **Фронтенд**: [http://localhost:5173](http://localhost:5173)
- **Административный интерфейс Django**: [http://localhost:8000/admin](http://localhost:8000/admin)
## Использование
1. Перейдите на главную страницу приложения.
2. Зарегистрируйтесь или войдите в систему.
3. Используйте интерфейс для загрузки, скачивания и управления файлами.
## Лицензия
Этот проект лицензирован под MIT License - подробности смотрите в файле [LICENSE](LICENSE).
## Контакты
Если у вас есть вопросы, вы можете связаться со мной по электронной почте: evgeniy@chausov.ru.
