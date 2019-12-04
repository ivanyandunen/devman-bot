import requests
from dotenv import load_dotenv
import os
import logging
import telegram


def get_review_info(token, timestamp=None):
    url = f'https://dvmn.org/api/long_polling/?timestamp={timestamp}'
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def send_message(bot, title, url, is_negative):
    lesson_link = f'<a href="https://dvmn.org{url}">{title}</a>.'
    if is_negative:
        message = 'К сожалению, в работе нашлись ошибки'
    else:
        message = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
    bot.send_message(
        chat_id,
        text=f'У вас проверили работу {lesson_link}\n\n{message}',
        parse_mode=telegram.ParseMode.HTML
        )


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    token = os.getenv('dvmn_API_token')
    bot_token = os.getenv('bot_API_token')
    chat_id = os.getenv('chat_id')
    pp = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:9150')
    bot = telegram.Bot(token=bot_token, request=pp)
    timestamp = None

    while True:
        try:
            if not timestamp:
                response = get_review_info(token)
                if response['status'] == 'timeout':
                    timestamp = response['timestamp_to_request']
                    response = get_review_info(token, timestamp)
                elif response['status'] == 'found':
                    send_message(
                        bot,
                        response['new_attempts'][0]['lesson_title'],
                        response['new_attempts'][0]['lesson_url'],
                        response['new_attempts'][0]['is_negative']
                        )
                else:
                    timestamp = None
        except requests.exceptions.ReadTimeout:
            logging.debug('Timeout')
            continue
        except ConnectionError:
            logging.debug('No connection')
            continue
        except KeyboardInterrupt:
            logging.debug('Connection closed by user')
            break
