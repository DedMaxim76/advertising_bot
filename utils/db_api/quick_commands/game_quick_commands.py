import asyncio
import datetime
import random
import aioschedule

from asyncpg import UniqueViolationError

from data import config
from utils.db_api.db_gino import db
from utils.db_api.schemas.games import Game


async def create_game():
    checker = True
    while checker:
        try:
            game_id = random.randint(10000000000, 99999999999)
            game = Game(id=game_id)
            await game.create()
            config.CURRENT_GAME_ID = game_id
            # aioschedule.every().friday.at("11:55").do(add_users_to_game)
            # aioschedule.every().friday.at("11:59").do(start_game)
            checker = False
        except UniqueViolationError:
            pass


async def select_all_games():
    games = await Game.query.gino.all()
    return games


async def count_games():
    total = await db.func.count(Game.id).gino.scalar()
    return total


async def select_game(user_id: int):
    game = await Game.get(user_id)
    if not game:
        return None
    return game


async def change_bank(game_id: int, bank: float):
    game = await Game.get(game_id)
    bank_temp = game.bank + bank
    if bank_temp < 0:
        bank_temp = 0
    await game.update(bank=bank_temp).apply()
