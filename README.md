# Devman bot

This is a telegram bot, which is used for getting notifications about lessons reviews.


## How to install

Python 3.7 has to be installed. You might have to run python3 instead of python depending on system if there is a conflict with Python2. Then use pip (or pip3) to install dependencies:

```commandline
pip install -r requirements.txt
```
## How to use

There are several parameters which have to be specified in `.env` file first:


`dvmn_API_token` from [Devman API documentation](https://dvmn.org/api/docs/)

`bot_API_token` is provided by [BotFather](https://telegram.me/BotFather) after creating your bot.

`chat_id` - your id in Telegram. Send message to @userinfobot in Telegram to get it.


To work behind a proxy specify your proxy address in variable `pp`

    pp = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:9150')

In the other case this variable should be deleted or commented.


Run `python main.py`


## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
