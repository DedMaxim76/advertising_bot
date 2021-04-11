from sqlalchemy import Integer, Column, BigInteger, String, Float, sql, Boolean

from utils.db_api.db_gino import TimedBaseModel


class Game(TimedBaseModel):
    __tablename__ = 'games'
    id = Column(BigInteger, primary_key=True)
    count_of_users = Column(Integer, default=0)
    bank = Column(Integer, default=0)

    query: sql.Select
