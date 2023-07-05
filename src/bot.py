import os
import logging
import time
import pytube
from pytube import YouTube
import os


from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram import Update

from downloader import download
from config import settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

ATTEMPTED_LOGINS = []
EXIT, MESSAGE = range(2)


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
        # Tempoorary replacement for database
        user_chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        if user_id != settings.ADMIN_ID:
            with open("users.txt", "a+") as file:
                file.seek(0)
                users = file.read()
                if str(user_chat_id) not in users:
                    file.write(str(user_chat_id) + "\n")
                    logger.info("New user registered: @%s", update.effective_user.username)
        

        title = download(url=update.message.text)
        with open(f"{title}.mp3", "rb") as audio:
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
        os.remove(f"{title}.mp3")
    except pytube.exceptions.RegexMatchError as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid link! Try again",
        )
        logger.warning('Update "%s" caused error "%s"', update, e)
    except Exception as e:
        logger.error('Update "%s" caused exception "%s"', update, e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error Occured! Contact Administrator",
        )


def send_all(update: Update, context: CallbackContext):
    if update.effective_user.id != settings.ADMIN_ID:
        return ConversationHandler.END
    update.message.reply_text("Send me the message you want to send to all users")
    return MESSAGE


def send_all_message(update: Update, context: CallbackContext):
    message = update.message.text
    with open("users.txt", "r") as file:
        users = file.readlines()

    for chat_id in users:
        context.bot.send_message(chat_id=chat_id, text=message, parse_mode="markdown")
    
    update.message.reply_text("Message has been sent to all users") 
    return ConversationHandler.END

def exit_conv(update: Update, context: CallbackContext):
    update.message.reply_text("Aborting sending the message")
    return ConversationHandler.END

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

    if not os.path.exists("users.txt"):
        file = open("users.txt", "w")
        file.close()

    updater = Updater(settings.TOKEN, use_context=True)

    dp = updater.dispatcher

    # add commands handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("send_all", send_all)],
            states={
                MESSAGE: [MessageHandler(Filters.text, send_all_message)],
                EXIT: [MessageHandler(Filters.text, exit_conv)],
            },
            fallbacks=[CommandHandler("exit", exit_conv)],
        )
    )

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
