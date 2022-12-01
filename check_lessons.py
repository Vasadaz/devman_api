import time
from pprint import pprint

import requests

from environs import Env


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
    print(response.url)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env.str('DEVMAN_TOKEN')
    timestamp = None

    while True:
        try:
            verifications = get_verification_results(token, timestamp)

            if verifications['status'] == 'found':
                timestamp = verifications['last_attempt_timestamp']
                pprint(verifications)
            else:
                timestamp = verifications['timestamp_to_request']
                print('Not Found', timestamp)
                pprint(verifications)
        except requests.exceptions.ReadTimeout as error:
            print(error)
        except requests.exceptions.ConnectionError as error:
            print(error)
            time.sleep(10)
