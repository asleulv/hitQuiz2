import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or '9n43r943i9m34ir95432c434f3'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///quiz.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
