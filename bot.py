"""
- send actual dorams by default query
- ask on the query with user's parameters: kind, data or rate
"""


import logging
import yaml
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from server import find_serials


# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# parsing config-file
with open('configuration/config_bot.yaml', 'r') as handle:
    configs = yaml.full_load(handle)

TOKEN = configs['token']


# bot actions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'Hi {update.message.chat.first_name}! Nice to see you here! \nWelcome to the world of doramas 🤍'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def random_dorama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = find_serials('random')
    text_items = ['Here is your random dorama from 2016 to 2024 and with a kinopoisk rating of over 7.1:\n']
    for j in ['Name', 'Description', 'KP rating', 'Genres', 'Countries']:
        if j == 'Name':
            item = f'[{answer[j]}]({answer["Link"]})'
        else:
            item = f'*{j}*: _{answer[j]}_'
        text_items.append(item)
    text_items.append('')
    text = '\n'.join(text_items)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')


async def last_doramas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = find_serials('last')
    if len(answer) == 0:
        text = "Unfortunately I can't find a good dorama for you now, but I'm still learning 🥺"
    else:
        text_items = ['Here are 5 best last doramas by Kinopoisk rating:\n']
        for i in range(len(answer)):
            for j in ['Name', 'KP rating', 'Genres', 'Countries']:
                if j == 'Name':
                    item = f'*{i + 1}.* [{answer[j][i]}]({answer["Link"][i]})'
                else:
                    item = f'*{j}*: _{answer[j][i]}_'
                text_items.append(item)
            text_items.append('')
        text = '\n'.join(text_items)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')


async def end(update: Update,  context: ContextTypes.DEFAULT_TYPE):
    text = f'Thanks for your politeness! Have a good day, {update.message.chat.first_name}!'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    last_doramas_handler = CommandHandler('last_doramas', last_doramas)
    application.add_handler(last_doramas_handler)

    random_dorama_handler = CommandHandler('random_dorama', random_dorama)
    application.add_handler(random_dorama_handler)

    end_handler = CommandHandler('end', end)
    application.add_handler(end_handler)

    application.run_polling()
