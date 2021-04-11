import asyncio

import aioschedule
from aiogram import executor

from data import config
from handlers.users.bonus_system import withdraw_weekly_bonus
from handlers.users.top import show_top
from loader import dp, bot
from utils.db_api import db_gino
from utils.db_api.db_gino import db
from utils.db_api.quick_commands import game_quick_commands


async def clear_table():
    print("Чистим базу")
    await db.gino.drop_all()
    print("Готово")
    print("Создаем таблицы")
    await db.gino.create_all()
    print("Готово")


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # import filters
    # import middlewares
    # filters.setup(dp)
    # middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")
    # await clear_table() # uncomment to clear DB and configure. COMMIT AFTER DONE!
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    # Запускает таймер для первой игры
    await game_quick_commands.create_game()
    asyncio.create_task(scheduler())
    aioschedule.every().friday.at("12:00").do(withdraw_weekly_bonus)
    aioschedule.every().day.at("19:00").do(show_top)
    await withdraw_weekly_bonus()


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)
