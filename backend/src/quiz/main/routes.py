from flask import (
	Blueprint, 
	current_app
)


blueprint = Blueprint(
	'main',
	__name__,
	url_prefix='/'
)

@blueprint.route('/')
def index():
	return current_app.send_static_file('index.html')