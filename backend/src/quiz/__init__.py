from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
	app = Flask(__name__, 
	    static_url_path = '',
	)
	app.config.from_object('quiz.config.Config')
	db.init_app(app)
	ma.init_app(app)
	migrate.init_app(app, db)

	register_blueprints(app)

	return app

def register_blueprints(app):
	from importlib import import_module
	mods = (
		('.main', {}),
		('.questions', {}),
		('.scores', {}),
	)
	for ident,kwargs in mods:
		module = import_module(ident, __name__)
		module.create_module(app, **kwargs)
