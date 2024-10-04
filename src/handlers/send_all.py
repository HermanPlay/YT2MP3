from config import cfg
from db import ClientDB
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler
from utils import get_logger

EXIT, MESSAGE = range(2)

logger = get_logger(__name__)


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != cfg.ADMIN_ID:
        return ConversationHandler.END
    await update.message.reply_text("Send me the message you want to send to all users")
    return MESSAGE


async def send_all_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text_html

    db = ClientDB()
    users = [user.user_id for user in db.get_users()]

    users.remove(cfg.ADMIN_ID)

    count = 0

    for chat_id in users:
        try:
            await context.bot.send_message(
                chat_id=chat_id, text=message, parse_mode=ParseMode.HTML
            )
            count += 1
        except Exception as e:
            logger.error('Update "%s" caused exception "%s"', update, e)
            db.disable_user(chat_id)
    await update.message.reply_text(
        f"Message has been sent to {count}/{len(users)} users"
    )
    await update.message.reply_text("See logs for more details")
    return ConversationHandler.END


async def exit_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aborting sending the message")
    return ConversationHandler.END


send_all_handler = ConversationHandler(
    entry_points=[CommandHandler("send_all", send_all)],
    states={
        MESSAGE: [MessageHandler(filters.TEXT, send_all_message)],
        EXIT: [MessageHandler(filters.TEXT, exit_conv)],
    },
    fallbacks=[CommandHandler("exit", exit_conv)],
)
