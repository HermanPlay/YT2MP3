from config import cfg
from telegram import Update
from telegram.ext import ContextTypes
from utils import get_logger

logger = get_logger(__name__)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log Errors caused by Updates.

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Error Occured! Contact here {cfg.SUPPORT_LINK}",
    )
    logger.warning('Update "%s" caused error "%s"', update, context.error)
