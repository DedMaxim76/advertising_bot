from aiogram import types
from aiogram.dispatcher.filters import BoundFilter, Filter

from data import config
from loader import bot


class IsChatMember(Filter):
    key = 'is_chat_member'

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(config.MAIN_CHANNEL_ID, message.from_user.id)
        return member.is_chat_member()

