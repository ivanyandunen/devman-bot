# Devman bot

This is a telegram bot, which is used for getting notifications about lessons reviews.


## How to install

Python 3.7 has to be installed. You might have to run python3 instead of python depending on system if there is a conflict with Python2. Then use pip (or pip3) to install dependencies:

```commandline
pip install -r requirements.txt
```
## How to use

<strong>Locally:</strong>

There are several parameters which have to be specified in `.env` file first:

`DVMN_API_TOKEN` from [Devman API documentation](https://dvmn.org/api/docs/)

`TG_BOT_API_TOKEN` is provided by [BotFather](https://telegram.me/BotFather) after creating your bot.

`TG_CHAT_ID` - your id in Telegram. Send message to @userinfobot in Telegram to get it.


Run `python main.py`

To work behind a proxy specify your proxy address `python main.py --proxy %proxy address%`

<strong>Deploying on Heroku:</strong>

For deploying you need to have `Procfile` in the repo's root on Github containing string:
```
bot python3 main.py
```
And the same variables from `.env` file added to Config Vars

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
