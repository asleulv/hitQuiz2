
def create_module(app, **kwargs):
	from .routes import blueprint
	app.register_blueprint(blueprint, **kwargs)
