import os
import logging

from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import Update

from downloader import download
from config import settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """
    Funciton replies to a /start command sent by user

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """

    update.message.reply_text("Hi! Send me link with audio, which has to be downloaded")


def help(update: Update, context: CallbackContext) -> None:
    """
    Funciton replies to a /help command sent by user

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    update.message.reply_text("Write /start")


def echo(update: Update, context: CallbackContext) -> None:
    """
    Funciton replies to user's message (assumed to be link)

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    try:
        title = download(url=update.message.text)
        with open(f"{title}.mp3", "rb") as audio:
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
        os.remove(f"{title}.mp3")
    except Exception as e:
        logger.error('Update "%s" caused exception "%s"', update, e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error Occured! Contact Administrator",
        )


def error(update: Update, context: CallbackContext) -> None:
    """
    Log Errors caused by Updates.

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """
    Function applies all the handlers and starts the bot
    """

    updater = Updater(settings.TOKEN, use_context=True)

    dp = updater.dispatcher

    # add commands handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if settings.POLLING:
        updater.start_polling()  # Good for local testing
    else:
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)),
            url_path=settings.TOKEN,
            webhook_url=settings.webhook_url,
        )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()