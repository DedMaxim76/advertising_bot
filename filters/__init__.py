from aiogram import Dispatcher

from loader import dp
from .IsChatMemberFilter import IsChatMember
from .IsAdminFilter import IsAdmin

if __name__ == "filters":
    dp.filters_factory.bind(IsChatMember)
    dp.filters_factory.bind(IsAdmin)
    pass
