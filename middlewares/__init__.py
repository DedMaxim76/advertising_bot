from aiogram import Dispatcher

from loader import dp
from .subscription import SubscriptionMiddleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(SubscriptionMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
