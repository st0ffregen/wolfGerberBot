#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import telegram
from dotenv import load_dotenv
import urllib.request
import logging
import json

load_dotenv()


def fetchApi(url):
    req = urllib.request.Request(url,
                                 data=None,
                                 headers={
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                 })

    return urllib.request.urlopen(req).read()


def getDates(response):
    return json.loads(response)['aps']


def createMessage(dates):
    message = 'Mögliche Termine:\n'
    for date in dates:
        message += 'Am ' + date['date'] + ' um ' + date['time'] + '\n'

    return message


def sendToTelegram(bot, chatId, text):
    bot.send_message(chat_id=chatId, text=text)


def configureLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    file_handler = logging.FileHandler('logs/wolfGerberBot.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def main():
    logger = configureLogger()

    logger.info('start wolf gerber bot')

    url = 'https://api.termed.de/v2/getEvents.php?action=free&time=8&id=1165&reason=undefined'

    token = os.environ['TELEGRAM_TOKEN']
    telegramChatId = os.environ['TELEGRAM_CHAT_ID']

    response = fetchApi(url)
    dates = getDates(response)

    if len(dates) > 0:
        message = createMessage(dates)
        logger.info('send ' + message + ' to telegram')
        bot = telegram.Bot(token=token)
        sendToTelegram(bot, telegramChatId, message)
    else:
        logger.info('no dates available')


if __name__ == "__main__":
    main()
