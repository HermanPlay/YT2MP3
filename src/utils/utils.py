import logging

from config.exceptions import UserNotFoundError
from db import ClientDB
from schemas import User


def get_logger(
    name: str,
    level: str = "INFO",
    log_to_file: bool = False,
    file_name: str = "app.log",
):
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Optional file handler
    if log_to_file:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        logger.addHandler(file_handler)

    # Create formatters and add them to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    if log_to_file:
        file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    return logger


def register_user(effective_user: dict) -> bool:
    """
    Function adds new user to the database

    :param effective_user: User object from Telegram API
    """
    db = ClientDB()
    user_id = effective_user.id
    username = effective_user.username
    if username is None:
        username = ""
    first_name = effective_user.first_name
    language_code = effective_user.language_code
    try:
        db.get_user(user_id)
    except UserNotFoundError:
        db.add_user(
            User(
                username=username,
                user_id=user_id,
                first_name=first_name,
                language_code=language_code,
            )
        )
        return True
    else:
        return False
