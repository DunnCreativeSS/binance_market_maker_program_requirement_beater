from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, backref
from model import Model
from connector import Postgresql


class Bots(Postgresql.Base, Model):
    __tablename__ = 'bots'

    id=Column(Integer, primary_key=True)
    type=Column('type', String)
    name=Column('name', String)