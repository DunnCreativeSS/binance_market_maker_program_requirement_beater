from connector import Postgresql

class Repository:
	Base = None
	Session = None

	"""docstring for Repository"""
	def __init__(self,Config):
		host = Config.get('connector.postgresql.host')
		username = Config.get('connector.postgresql.username')
		password = Config.get('connector.postgresql.password')
		port = Config.get('connector.postgresql.port')
		db = Config.get('connector.postgresql.db')

		psql = Postgresql(username, password, host, port, db)
		self.Session = psql.Session
		self.Base = psql.Base

		psql.Base.metadata.create_all(psql.engine, checkfirst=True)

	def Save(self,model):
		self.Session.add(model)
		self.Session.commit()
		self.Session.flush()
		# self.Session.close()
		self.Session.refresh(model)
		return model

	def Update(self):
		self.Session.commit()
		self.Session.flush()
		# self.Session.close()

	def GetSession(self):
		return self.Session