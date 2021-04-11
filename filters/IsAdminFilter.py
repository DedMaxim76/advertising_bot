from aiogram import types
from aiogram.dispatcher.filters import Filter

from data import config
from loader import bot


class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: types.Message):
        if str(message.from_user.id) == config.ADMINS[0]:
            return True
        else:
            return False

