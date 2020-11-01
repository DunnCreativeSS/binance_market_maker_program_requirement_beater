from random import random
import datetime
from model import AccountsTrades
from repositories.repository import Repository


class TradesRepo(Repository):
	Session = None
	"""TradesRepo is for defining every action on their user account"""
	def __init__(self,cfg):
		super(TradesRepo, self).__init__(cfg)
		self.Session = super().GetSession()

	def NewPositionOpen(self,accountID):
		# insert into account_trades
		modelAccTrade = AccountsTrades()
		modelAccTrade.account = accountID
		modelAccTrade.type = "crypto"
		modelAccTrade.pairs = "XLM/USDT"
		modelAccTrade.avep = 23.23
		modelAccTrade.size = 2.23
		modelAccTrade.open = datetime.datetime.now()

		saved = super().Save(modelAccTrade)
		return saved

	def UpdatePositionTrades(self, accountTradesID):
		self.Session.query(AccountsTrades).filter(AccountsTrades.id==accountTradesID).\
        									update({"avep":random(), "size":random()})
		super().Update()


	def ClosePositionTrades(self,accountTradesID):
		self.Session.query(AccountsTrades).filter(AccountsTrades.id==accountTradesID).\
								update({"closed":datetime.datetime.now()})
		super().Update()

	def GetTrades(self):
		return self.Session.query(AccountsTrades).first()