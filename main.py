import requests
import os
import logging
import telegram
import argparse


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy', help='Specify proxy address', default=None)
    return parser.parse_args()


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
    logging.basicConfig(level=logging.DEBUG)
    token = os.environ['DVMN_API_TOKEN']
    bot_token = os.environ['TG_BOT_API_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']

    if get_parser_args().proxy:
        pp = telegram.utils.request.Request(proxy_url=proxy_url)
        bot = telegram.Bot(token=bot_token, request=pp)
    else:
        bot = telegram.Bot(token=bot_token)

    timestamp = None

    while True:
        try:
            response = get_review_info(token, timestamp)
            if response['status'] == 'timeout':
                timestamp = response['timestamp_to_request']
            elif response['status'] == 'found':
                answer = response['new_attempts'][0]
                send_message(
                    bot,
                    answer['lesson_title'],
                    answer['lesson_url'],
                    answer['is_negative']
                    )
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
