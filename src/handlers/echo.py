import os

import locales
import pytubefix
from config.exceptions import FileTooLarge
from downloader import download
from downloader import fix_metadata
from telegram import Update
from telegram.constants import ChatAction
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler
from utils import get_logger
from utils import register_user

logger = get_logger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Funciton replies to user's message (assumed to be link)

    :param update: Containts incoming update, usually message
    :param context: Context object passed to the callback by CommandHandler
    """
    try:
        register_user(update.effective_user)

        msg = await update.message.reply_text("Downloading...")
        download_result = download(url=update.message.text)
        await msg.delete()
        msg = await update.message.reply_text("Making adjustments...")
        title = fix_metadata(
            file_name=download_result.file_name, file_path=download_result.file_path
        )
        await msg.delete()
        msg = await update.message.reply_text("Sending audio...")
        with open(f"{title}.mp3", "rb") as audio:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VOICE
            )
            await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=audio,
                filename=f"{download_result.title}.mp3",
                caption=locales.US_SUCCESSFUL_DOWNLOAD_TEXT,
                parse_mode=ParseMode.HTML,
            )
        os.remove(f"{title}.mp3")
        await msg.delete()
    except pytubefix.exceptions.RegexMatchError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid link! Try again",
        )
    except FileTooLarge:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=locales.US_TOO_LONG_VIDEO_TEXT
        )
    except Exception as e:
        raise e


echo_handler = MessageHandler(filters.TEXT, echo)
