import tempfile
import viper

yaml_example = b'''
connector:
 postgresql:
   host: 0.0.0.0
   username: default3
   password: w0rdp4ss
   port: 5432
   db: xtremex
'''

class ConfigEnvironment:
	"""docstring for Config"""
	def __init__(self):
		super(ConfigEnvironment, self).__init__()
	
	def New(self):
		with tempfile.NamedTemporaryFile(suffix='.yaml') as temp:
			temp.write(yaml_example)
			temp.seek(0)
			viper.set_config_path(temp.name)
			viper.read_config()
			return viper