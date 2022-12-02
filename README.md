# Бот для получения уведомлений от Devman
 
Проект `devman_bot` мониторит результат проверки работ и отправляет уведомление 
о них в Telegram.


## Как установить

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Vasdaz/devman_bot.git
    ```

2. Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```

3. [Получить токен Devman.](https://dvmn.org/api/docs/)

5. [Получить токен Телеграм бота.](https://telegram.me/BotFather)

6. [Получить свой ID.](https://t.me/userinfobot)

6. Создать файл `.env` с данными:
    ```dotenv
    DEVMAN_TOKEN=токен Devman
    TELEGRAM_TOKEN=токен Телеграм бота
    TELEGRAM_CHAT_ID=свой ID
    ```

7. Запуск бота:
    
    ```shell
    python3 check_lessons.py
    ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
