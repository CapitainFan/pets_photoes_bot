import logging
import os
import requests
import random
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv 

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


URL1 = 'https://api.thedogapi.com/v1/images/search'
URL2 = 'https://api.thecatapi.com/v1/images/search'


def get_new_dog_image():
    response = requests.get(URL1)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def get_new_cat_image():
    response = requests.get(URL2)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_dog_image())

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_cat_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/newcat'], ['/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри кого я тебе нашел'.format(name),
        reply_markup=buttons,
    )

    if random.choice([1, 2, 3, 4]) > 2:
        context.bot.send_photo(chat.id, get_new_dog_image())
    else:
        context.bot.send_photo(chat.id, get_new_cat_image())


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
