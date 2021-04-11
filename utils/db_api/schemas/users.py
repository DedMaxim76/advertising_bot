from sqlalchemy import Integer, Column, BigInteger, String, Float, sql, Boolean

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100))
    username = Column(String(32))
    balance = Column(Float, default=0)
    phone = Column(String(30), default=None)
    card = Column(String(16), default=None)
    referral_code = Column(String(8), default=None)
    inviter_code = Column(String(), default=None)
    num_of_active_referrals = Column(Integer, default=0)
    num_of_passive_referrals = Column(Integer, default=0)
    bonus_referrals = Column(Integer, default=0)
    in_game = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)

    query: sql.Select
