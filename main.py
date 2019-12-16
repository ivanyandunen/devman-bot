import requests
from dotenv import load_dotenv
import os
import logging
import telegram


def get_review_info(token, timestamp=None):
    url = 'https://dvmn.org/api/long_polling'
    payload = {'timestamp': timestamp}

    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
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
    token = os.getenv('DVMN_API_TOKEN')
    bot_token = os.getenv('TG_BOT_API_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    proxy_url = os.getenv('PROXY_URL')

    if proxy_url:
        pp = telegram.utils.request.Request(proxy_url=proxy_url)
        bot = telegram.Bot(token=bot_token, request=pp)
    else:
        bot = telegram.Bot(token=bot_token)

    timestamp = None

    while True:
        try:
            if not timestamp:
                response = get_review_info(token)
                if response['status'] == 'timeout':
                    timestamp = response['timestamp_to_request']
                    response = get_review_info(token, timestamp)
                elif response['status'] == 'found':
                    answer = response['new_attempts'][0]
                    send_message(
                        bot,
                        answer['lesson_title'],
                        answer['lesson_url'],
                        answer['is_negative']
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
        except requests.exceptions.HTTPError:
            logging.debug('404 Client Error')
            break
