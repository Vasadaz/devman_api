from pprint import pprint

import requests

from environs import Env


def get_lessons(token: str) -> dict:
    headers = {'Authorization': f'Token {token}'}
    url = 'https://dvmn.org/api/user_reviews/'

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_verification_results(token: str) -> dict:
    headers = {'Authorization': f'Token {token}'}
    url = 'https://dvmn.org/api/long_polling/'

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env.str('DEVMAN_TOKEN')

    lessons = get_lessons(token)
    pprint(lessons)

    while True:
        verifications = get_verification_results(token)
        pprint(verifications)
