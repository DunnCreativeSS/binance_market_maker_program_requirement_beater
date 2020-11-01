from model import Users, Accounts
from repositories.repository import Repository


class UsersRepo(Repository):
	Session = None
	"""UsersRepo is for defining every action on their user account"""
	def __init__(self,cfg):
		super(UsersRepo, self).__init__(cfg)
		self.Session = super().GetSession()
		
	# RegisterUser is for create new user
	def RegisterUser(self,email,telegram,referral,affiliate,affshare,term,fee,payment,access, botID):
		userModel = Users()
		userModel.email = email
		userModel.telegram = telegram
		if referral is not None:
			userModel.referral = referral
		userModel.affiliate = affiliate
		userModel.affshare = affshare
		userModel.term = term
		userModel.fee = fee
		userModel.payment = payment
		userModel.access = access
		super().Save(userModel)

		accountModel = Accounts()
		accountModel.rel_user = userModel
		accountModel.type = "crawler"
		accountModel.bot = botID
		accountModel.pub = "pubg"
		accountModel.pri = "primal"
		accountModel.active = True
		accountModel.deposit = "3321"

		super().Save(accountModel)
		return userModel

	def GetOneUser(self):
		return self.Session.query(Users).first()