import logging
import time

import requests
import telegram

from environs import Env

from bot_logger import BotLogsHandler

logger = logging.getLogger(__file__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()
    dvm_token = env.str('DEVMAN_TOKEN')
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    tg_chat_id = env.str('TELEGRAM_CHAT_ID')
    tg_bot_name = env.str('TELEGRAM_BOT_NAME', '')
    admin_tg_token = env.str('TELEGRAM_ADMIN_BOT_TOKEN', '')
    admin_tg_chat_id = env.str('TELEGRAM_ADMIN_CHAT_ID', '')
    timestamp = None
    bot = telegram.Bot(tg_token)

    if not tg_bot_name:
        tg_bot_name = f'@{bot.get_me().username}'
    else:
        tg_bot_name += f' @{bot.get_me().username}'

    if not admin_tg_token:
        admin_tg_token = tg_token

    if not admin_tg_chat_id:
        admin_tg_chat_id = tg_chat_id

    logger.addHandler(BotLogsHandler(tg_bot_name, admin_tg_token, admin_tg_chat_id))
    logger.info('Start Devman bot.')

    while True:
        try:
            logging.info('Devman bot checking lessons.')
            headers = {'Authorization': f'Token {dvm_token}'}
            params = {'timestamp': timestamp}
            url = 'https://dvmn.org/api/long_polling/'

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            verifications = response.json()

            if verifications['status'] == 'found':
                results = verifications['new_attempts']

                for result in results:
                    msg = f'Есть проверенная работа "{result["lesson_title"]}"\n{result["lesson_url"]}\n\n'

                    if result['is_negative']:
                        msg += 'Есть ошибки...'
                    else:
                        msg += 'Работа успешно принята!!!'

                    bot.send_message(chat_id=tg_chat_id, text=msg)

                timestamp = verifications['last_attempt_timestamp']
            else:
                timestamp = verifications['timestamp_to_request']
        except requests.exceptions.ReadTimeout as error:
            logging.info(f'Devman bot not found any new proven lessons..')
        except requests.exceptions.ConnectionError as error:
            logging.error(f'Devman bot {error}')
            time.sleep(60)
        except Exception as err:
            logger.exception(f'Unexpected error - {err}:\n\n')
            time.sleep(60)
