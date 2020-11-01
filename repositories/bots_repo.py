from model import Bots,AccountsTrades
from repositories.repository import Repository


class BotsRepo(Repository):
	Session = None
	"""BotsRepo is for defining bots action"""
	def __init__(self,cfg):
		super(BotsRepo, self).__init__(cfg)
		self.Session = super().GetSession()

		
	# Register is for creating new bot
	def RegisterBot(self,name,type):
		botModel = Bots()
		botModel.name = name
		botModel.type = type 

		super().Save(botModel)
		return botModel

	def GetOneBot(self):
		return self.Session.query(Bots).first()

	def GetAllPairs(self):
		return self.Session.query(AccountsTrades.pairs).group_by(AccountsTrades.pairs).all()