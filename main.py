import requests
import os
import logging
import telegram
import argparse


class TgHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id, text=log_entry)


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy', help='Specify proxy address')
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
    token = os.environ['DVMN_API_TOKEN']
    bot_token = os.environ['TG_BOT_API_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    proxy_url = get_parser_args().proxy
    if proxy_url:
        pp = telegram.utils.request.Request(proxy_url=proxy_url)
        bot = telegram.Bot(token=bot_token, request=pp)
    else:
        bot = telegram.Bot(token=bot_token)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = TgHandler(bot, chat_id)
    formatter = logging.Formatter('%(levelname)s  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    timestamp = None

    logger.info('The bot has started')

    while True:
        try:
            response = get_review_info(token, timestamp)
            if response['status'] == 'timeout':
                timestamp = response['timestamp_to_request']
            elif response['status'] == 'found':
                answer = response['new_attempts'][0]
                print(answer)
                send_message(
                    bot,
                    answer['lesson_title'],
                    answer['lesson_url'],
                    answer['is_negative']
                    )
                timestamp = None

        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout')
            continue
        except ConnectionError:
            logger.warning('No connection')
            continue
        except KeyboardInterrupt:
            logger.warning('Connection closed by user')
            break
        except requests.exceptions.HTTPError:
            logger.warning('404 Client Error')
            break
