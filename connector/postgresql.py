from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Postgresql():

	Base = declarative_base()
	Session = None
	Engine = None
	"""docstring for Postgresql"""
	def __init__(self,username,password,host,port,db):
		super(Postgresql, self).__init__()
		self.engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(username,password,host,port,db))
		self.Session = sessionmaker(bind=self.engine)
		self.Session.configure(bind=self.engine)
		self.Session = self.Session()