from config import cfg
from db import ClientDB
from handlers import echo_handler
from handlers import error
from handlers import help_handler
from handlers import send_all_handler
from handlers import start_handler
from telegram.ext import ApplicationBuilder
from telegram.ext import BaseHandler
from utils import get_logger

# Enable logging
_logger = get_logger(__name__)
db = ClientDB()


class Application:
    def __init__(self) -> None:
        self.__token = cfg.TOKEN
        self.application = ApplicationBuilder().token(self.__token).build()

        self.add_handler(start_handler)
        self.add_handler(help_handler)
        self.add_handler(send_all_handler)
        self.add_handler(echo_handler)
        self.application.add_error_handler(error)

    def add_handler(self, handler: BaseHandler):
        self.application.add_handler(handler)

    def run(self):
        if cfg.ENV == "DEV":
            _logger.info("Setting polling")
            self.application.run_polling()
        else:
            _logger.info("Setting webhook")
            self.application.run_webhook(
                listen="0.0.0.0",
                port=cfg.PORT,
                url_path=cfg.TOKEN,
                webhook_url=cfg.WEBHOOK_URL + cfg.TOKEN,
            )
