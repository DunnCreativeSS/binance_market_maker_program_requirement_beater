from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref
from model import Model
from connector import Postgresql


class Users(Postgresql.Base, Model):
    __tablename__ = 'users'

    id=Column(Integer, primary_key=True)
    email=Column('email', String)
    telegram=Column('telegram', String)
    referral=Column('referral',  Integer, ForeignKey('users.id'))
    referral_user=relationship("Users")
    rel_accounts=relationship("Accounts")
    affiliate=Column('affiliate', String)
    affshare=Column('affshare', Integer)
    term=Column('term', String)
    fee=Column('fee', Numeric)
    payment=Column('payment', String)
    access=Column('access', Integer)