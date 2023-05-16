from .. import db
from .models import Score
from .schemas import ScoreSchema
from flask import (
	Blueprint, 
	jsonify, 
	request, 
	session
)
import re


blueprint = Blueprint(
	'scores',
	__name__,
	url_prefix='/scores'
)

@blueprint.route('/')
def index():
	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
	scores_schema = ScoreSchema(many=True)
	return scores_schema.jsonify(scores)

@blueprint.post('/')
def create():
	name = request.json.get('name', '')
	points = session.get('points', 0)

	# use webargs
	if points >= 50 \
		and 3 <= len(name.strip()) <= 8 \
		and re.match(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*', name.strip()):
		
		score = Score(name=name, points=points)
		db.session.add(score)
		db.session.commit()

	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
	scores_schema = ScoreSchema(many=True)
	return scores_schema.jsonify(scores)
