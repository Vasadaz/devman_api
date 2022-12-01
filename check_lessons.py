import time
from pprint import pprint

import requests

from environs import Env

from telegram_bot import send_msg


def get_lessons(token: str) -> dict:
    headers = {'Authorization': f'Token {token}'}
    url = 'https://dvmn.org/api/user_reviews/'

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_verification_results(token: str, timestamp: float) -> dict:
    headers = {'Authorization': f'Token {token}'}
    params = {
        'timestamp': timestamp,
    }
    url = 'https://dvmn.org/api/long_polling/'

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=120,
    )
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    dvm_token = env.str('DEVMAN_TOKEN')
    tg_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TELEGRAM_CHAT_ID')
    timestamp = None

    while True:
        try:
            verifications = get_verification_results(dvm_token, timestamp)

            if verifications['status'] == 'found':
                tg_msg = verifications['new_attempts']
                send_msg(
                    token=tg_token,
                    chat_id=tg_chat_id,
                    msg=tg_msg
                )
                print(tg_msg)
                timestamp = verifications['last_attempt_timestamp']
            else:
                timestamp = verifications['timestamp_to_request']
        except requests.exceptions.ReadTimeout as error:
            print(error)
        except requests.exceptions.ConnectionError as error:
            print(error)
            time.sleep(10)
