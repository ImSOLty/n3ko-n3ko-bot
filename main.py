import os
import random

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import requests

COUNT = 1
API_FAILED_MESSAGE = 'API wequest f-faiwed *:･ﾟ✧*:･ﾟ✧  i don\'t know the weason ¯\\_(ツ)_/¯'
HELP_MESSAGE = '''Wew, it is a simple t-test b-bot,,, that has multiple
commands, that will send you a pretty neko〜☆:
{list_of_commands}'''

API_URL = 'https://nekos.best/api/v2/{query}'
TOKEN = os.getenv("TELEGRAM_TOKEN")


def get_all_commands():
    req_result = requests.get(API_URL.format(query="endpoints"))
    if req_result.status_code == 200:  # OK
        json_result = req_result.json()
        return {command: json_result[command]["format"] for command in json_result.keys()}
    raise requests.RequestException()


ALL_COMMANDS = get_all_commands()


def get_neko(category="neko"):
    req_result = requests.get(API_URL.format(query=category))
    if req_result.status_code == 200:
        return ALL_COMMANDS[category], req_result.json()['results'][0]['url']
    return None, None


async def show_neko(update: Update, context: ContextTypes.DEFAULT_TYPE, result):
    if result[0] == "png":
        await context.bot.send_photo(update.message.chat_id, result[1])
    elif result[0] == "gif":
        await context.bot.send_video(update.message.chat_id, result[1])
    else:
        await update.message.reply_text(API_FAILED_MESSAGE)


async def neko(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    category = update.message.text[1:]  # Cut off the slash symbol
    await show_neko(update, context, get_neko(category))


async def random_neko(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_neko(update, context, get_neko(random.choice(ALL_COMMANDS)))


async def helpy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_MESSAGE.format(list_of_commands='\n'.join(
        f'/{command}' for command in ALL_COMMANDS.keys()
    )))


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    for category, content_type in ALL_COMMANDS.items():
        app.add_handler(CommandHandler(category, neko))
    app.add_handler(CommandHandler("help", helpy))
    app.add_handler(CommandHandler("random", random_neko))

    app.run_polling()


if __name__ == "__main__":
    main()
