from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Funciton replies to a /help command sent by user

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    await update.message.reply_text("Write /start")


help_handler = CommandHandler("help", help)
