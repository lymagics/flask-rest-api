import json
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def read_config():
	"""Read database configuration."""
	with open('config.json') as json_config:
		config = json.load(json_config)

	if config.get('mysql', False):
		my_sql_config = config['mysql']
		hostname = my_sql_config['host']
		username = my_sql_config['username']
		password = my_sql_config['password']
		database = my_sql_config['database']

		connection_string = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'
		return create_engine(connection_string, echo=True)
	else:
		raise KeyError('Wrong config file.')


Base = declarative_base()
engine = read_config()
Session = sessionmaker(bind=engine)


def create_database(engine):
	"""Create database tables."""
	Base.metadata.create_all(engine)


def create_app():
	"""Create flask application."""
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'random secure key'

	from .views import views, URL
	app.register_blueprint(views, url_prefix=URL)

	from .models import User, Address
	create_database(engine)

	return app 