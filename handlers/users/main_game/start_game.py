import asyncio
import random

import aioschedule

from data import config
from keyboards.inline.account_inline_menu import game_info_menu
from loader import bot
from utils.db_api.quick_commands import user_quick_commands, game_quick_commands


async def start_game():
    print("GAME STARTED")
    users: dict = await user_quick_commands.select_users_in_game()
    users_sum_of_win: dict = {}
    if users is None:
        aioschedule.clear()
        await game_quick_commands.create_game()
        return
    count_of_users = len(users)
    for i in range(1, count_of_users+1):
        users_sum_of_win[i] = 0
    print(users_sum_of_win)
    await game_quick_commands.change_bank(config.CURRENT_GAME_ID, count_of_users)
    for i in range(count_of_users):
        winner_number = random.randint(1, count_of_users)
        if winner_number in users_sum_of_win:
            users_sum_of_win[winner_number] += 1
        else:
            users_sum_of_win[winner_number] = 1
    print(users_sum_of_win)
    for user_number, win in users_sum_of_win.items():
        await user_quick_commands.change_balance(users[user_number-1].id, win)
        await bot.send_message(chat_id=users[user_number-1].id,
                               text=f"""Мини игра RM завершена!

Ваш выигрыш: {win} монет
В игре было: {count_of_users} участников
""",
                               reply_markup=game_info_menu)
    await game_quick_commands.create_game()


async def add_users_to_game():
    users: dict = await user_quick_commands.select_all_users()
    for user in users:
        if user.balance >= 1:
            await user_quick_commands.change_balance(user.id, -1)
            await user_quick_commands.add_to_game(user.id)
            await bot.send_message(chat_id=user.id,
                                   text="Началась мини игра RM! С вашего баланса списалось 1 монета.",
                                   reply_markup=game_info_menu)