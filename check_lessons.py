import time

import requests

from environs import Env
from telegram_bot import send_msg


if __name__ == '__main__':
    env = Env()
    env.read_env()
    dvm_token = env.str('DEVMAN_TOKEN')
    tg_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TELEGRAM_CHAT_ID')
    timestamp = None

    while True:
        try:
            headers = {'Authorization': f'Token {dvm_token}'}
            params = {'timestamp': timestamp}
            url = 'https://dvmn.org/api/long_polling/'

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=120,
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

                    send_msg(
                        token=tg_token,
                        chat_id=tg_chat_id,
                        msg=msg,
                    )
                timestamp = verifications['last_attempt_timestamp']
            else:
                timestamp = verifications['timestamp_to_request']
        except requests.exceptions.ReadTimeout as error:
            print(error)
        except requests.exceptions.ConnectionError as error:
            print(error)
            time.sleep(60)
