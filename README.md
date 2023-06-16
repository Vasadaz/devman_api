# Бот для получения уведомлений от Devman
 
Проект `devman_bot` мониторит результат проверки работ и отправляет уведомление 
о них в Telegram.


## Как установить

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Vasadaz/devman_bot.git
    ```

2. Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```

3. [Получить токен Devman.](https://dvmn.org/api/docs/)

5. [Получить токен Телеграм бота.](https://telegram.me/BotFather)

6. [Получить свой ID.](https://t.me/userinfobot)

6. Создать файл `.env` с данными:
    - Обязательные
    ```dotenv
    DEVMAN_TOKEN=81ea0f38...ca3f # Токен Девмана
    TELEGRAM_BOT_TOKEN=581247650:AAH...H7A # Токен основного бота Telegram.
    TELEGRAM_CHAT_ID=123456789 # Ваш id Telegram, сюда будут отправлятся отправляться события проверки.
    ```
   
    - Необязательные переменные для логирования.
    ```dotenv
    TELEGRAM_ADMIN_BOT_TOKEN=5934478120:AAF...4X8 # Токен бота Telegram для отправки сообщений об ошибках.
    TELEGRAM_ADMIN_CHAT_ID=123456789 # Ваш id Telegram, сюда будут отправлятся сообщения об ошибках.
    TELEGRAM_BOT_NAME="Бот для проверки уроков" # Произвольное будет добавленно к его @username основного бота.
    ```

7. Запуск бота:
    ```shell
    python3 run_check_lessons.py
    ```


## Как запустить приложение в контейнере Docker

1. [Установить Docker Engine на сервер](https://docs.docker.com/engine/install/ubuntu/).

2. Перейти в директорию проекта `devman_bot`.

3. Соберите к образ Docker:
    ```shell
    docker build -t devman_bot .
    ```

4. Запустите контейнер с образом devman_bot:
   ```shell
    docker run devman_bot
    ```

5. Теперь бот работает в своём контейнере Docker.


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
