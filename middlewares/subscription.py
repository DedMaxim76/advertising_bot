from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.markdown import hlink

from data import config
from loader import bot


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        super(SubscriptionMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if message.text != "/start":
            user = message.from_user
            response = await bot.get_chat_member(config.MAIN_CHANNEL_ID, user.id)
            if not response.is_chat_member():
                await message.answer(f"Вы не подписаны на новостной канал: "
                                     f"{hlink('Vital Change...',config.MAIN_CHANNEL_URL)}")
                raise CancelHandler()