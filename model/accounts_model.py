from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, backref
from model import Model
from connector import Postgresql


class Accounts(Postgresql.Base, Model):
    __tablename__ = 'accounts'

    id=Column(Integer, primary_key=True)
    user=Column('referral',  Integer, ForeignKey('users.id'))
    rel_user=relationship("Users")
    type=Column('type', String)
    bot=Column('bot', Integer, ForeignKey('bots.id'))
    rel_bot=relationship("Bots")
    pub=Column('pub', String)
    pri=Column('pri', String)
    active=Column('active', Boolean)
    deposit=Column('deposit', String)
