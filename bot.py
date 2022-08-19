import os
import logging
import telegram

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from downlaoder import download

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', '8443'))
ROOT = os.path.dirname(__file__)
TOKEN = '5724767134:AAEYoGavRJU8tBXaU_3sZBuRM0GUEG2Lr3k'


def start(update, context):
    
    update.message.reply_text('Hi! Send me link with audio, which has to be downloaded')

def help(update, context):
    
    update.message.reply_text('Write /start')

def echo(update, context):
    bot = telegram.Bot(token=TOKEN)
    text_for_image = update.message.text
    image = imaging.draw_image(text_for_image)
    chatid = update.message.chat_id
    bot.send_photo(chat_id=chatid, photo=image)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN,
    #                       webhook_url="https://kindgaulek-bot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()