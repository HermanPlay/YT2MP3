from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from utils import get_logger
from utils import register_user

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Funciton replies to a /start command sent by user

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    await update.message.reply_text(
        "Hi! Send me link with audio, which has to be downloaded"
    )
    if register_user(update.effective_user):
        logger.info(f"New user registered: {update.effective_user.id=}")


start_handler = CommandHandler("start", start)
