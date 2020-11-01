from connector import Postgresql, ConfigEnvironment
from repositories import UsersRepo, BotsRepo, TradesRepo

if __name__ == '__main__':
	cfg = ConfigEnvironment()
	Config = cfg.New()
	
	# For Getting Bot
	repoBot = BotsRepo(Config)
	robot = repoBot.GetOneBot()
	if robot is None:
		botModel = repoBot.RegisterBot(name="cisada",type="painkiller")
		robot = repoBot.GetOneBot()
	print(robot.name)

	# Create User if not exist
	repoUser = UsersRepo(Config)
	user = repoUser.GetOneUser()
	if user is None:
		userModel = repoUser.RegisterUser(email='hendri@aruna.id',
											telegram='telegram',
											referral=None,
											affiliate='affiliate',
											affshare=3,
											term='term',
											fee=393.3,
											payment='payment',
											access=33,
											botID=robot.id)
				
		user = repoUser.GetOneUser()

	# Create Trades if not exist
	repoTrades = TradesRepo(Config)
	accTradesData =  repoTrades.GetTrades()
	if accTradesData is None:
		accTrades = repoTrades.NewPositionOpen(user.rel_accounts[0].id)
		accTradesData =  repoTrades.GetTrades()

	print(accTradesData.id)
	repoTrades.UpdatePositionTrades(accTradesData.id)
	repoTrades.ClosePositionTrades(accTradesData.id)

	# Get All Pairs
	pairs = repoBot.GetAllPairs()
	print(pairs)