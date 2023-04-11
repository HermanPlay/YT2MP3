import os
import logging

from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters
from downloader import download

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
ROOT = os.path.dirname(__file__)


async def save_to_db(update, context):
    pass


async def start(update, context):

    await update.message.reply_text(
        "Hi! Send me link with audio, which has to be downloaded"
    )
    # TODO: 1. Check if this is first time user uses bot, and if yes add to db


async def help(update, context):

    await update.message.reply_text("Write /start")


async def echo(update, context):
    try:
        title = download(url=update.message.text)
        with open(f"{title}.mp3", "rb") as audio:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
            await save_to_db(update, context)
        os.remove(f"{title}.mp3")
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error Occured! Contact Administrator",
        )


async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def setup():
    if not os.path.isdir("/db"):
        os.mkdir("/db")


def main():

    TOKEN = os.environ.get("TOKEN", "")

    #setup()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT, echo))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    # application.run_polling()
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url="https://yt2mp3-bot.herokuapp.com/" + TOKEN,
    )


if __name__ == "__main__":
    main()
