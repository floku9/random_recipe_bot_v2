import abc
from typing import Optional

from sqlalchemy.orm import session
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes

import resources.enums
from db import models


class BaseHandler(abc.ABC):
    def __init__(self, db_session: session):
        self._db_session = db_session
        self._db_user: Optional[models.User] = None
        self._db_conversation: Optional[models.Conversation] = None

    @abc.abstractmethod
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplementedError

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        tg_user = update.effective_user

        db_user = self._db_session.query(models.User).filter_by(telegram_id=tg_user.id).first()
        if not db_user:
            db_user = models.User(telegram_id=tg_user.id, name=tg_user.full_name)
            self._db_session.add(db_user)
            self._db_session.commit()
        self._db_user = db_user

        self._db_conversation = (
            self._db_session.query(models.Conversation)
            .filter(
                models.Conversation.user_id == db_user.id,
                models.Conversation.state != models.ConversationStates.END,
            )
            .first()
        )

        await self.handle(update=update, context=context)


class StartHandler(BaseHandler):
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._db_conversation:
            self._db_conversation = models.Conversation(
                user_id=self._db_user.id, state=resources.enums.ConversationStates.START
            )
            self._db_session.add(self._db_conversation)
            self._db_session.commit()

        await update.message.reply_text(
            f"Привет, {self._db_user.name}!\n"
            f"Я рецептный бот, и помогу тебе выбрать случайный рецепт, "
            f"согласно твоим предпочтениям"
        )


def init_handlers(app: Application, db_session: session) -> None:
    app.add_handler(CommandHandler("start", StartHandler(db_session=db_session)))
