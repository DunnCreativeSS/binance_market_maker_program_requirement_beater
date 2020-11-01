from sqlalchemy import Column, String, Integer, DateTime, Table, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, backref
from model import Model
from connector import Postgresql


class AccountsTrades(Postgresql.Base, Model):
    __tablename__ = 'accounts_trades'

    id=Column(Integer, primary_key=True)
    account=Column('account', Integer,ForeignKey('accounts.id'))
    rel_accounts=relationship("Accounts", backref="accounts_trades")
    pairs=Column('pairs', String)
    avep=Column('avep', Numeric)
    exit=Column('exit', Numeric)
    size=Column('size', Numeric)
    upnl=Column('upnl', Numeric)
    opened=Column('opened', DateTime)
    closed=Column('closed', DateTime)