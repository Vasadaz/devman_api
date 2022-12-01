from environs import Env
import telegram


def send_msg(token: str, chat_id: str, msg: str = ''):
    bot = telegram.Bot(token)
    user = bot.get_chat(chat_id=chat_id)

    if not msg:
        msg = f'Hellow, {user.first_name}!'

    bot.send_message(chat_id=chat_id, text=msg)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env.str('TELEGRAM_TOKEN')
    chat_id = env.str('TELEGRAM_CHAT_ID')

    send_msg(token, chat_id)
