import logging
import time

import requests
import telegram

from environs import Env


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Start Devman bot.')

    env = Env()
    env.read_env()
    dvm_token = env.str('DEVMAN_TOKEN')
    tg_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TELEGRAM_CHAT_ID')
    timestamp = None

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

                    bot = telegram.Bot(tg_token)
                    bot.send_message(chat_id=tg_chat_id, text=msg)

                timestamp = verifications['last_attempt_timestamp']
            else:
                timestamp = verifications['timestamp_to_request']
        except requests.exceptions.ReadTimeout as error:
            logging.error(f'Devman bot: {error}')
        except requests.exceptions.ConnectionError as error:
            logging.error(f'Devman bot: {error}')
            time.sleep(60)
