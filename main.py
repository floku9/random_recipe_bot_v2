import configparser
from pathlib import Path

import telegram.ext as tg_ext

from bot.handlers import init_handlers
from db.setup import get_session

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(Path("resources", "config.ini"))

    session = get_session(connections_string=config["db"]["connection_string"])
    app = tg_ext.Application.builder().token(config["bot"]["token"]).build()

    init_handlers(app=app, db_session=session)
    app.run_polling()
