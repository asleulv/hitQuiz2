from .. import db
from .models import Score
# from .schemas import ScoreSchema
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

# @blueprint.route('/')
# def index():
# 	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
# 	scores_schema = ScoreSchema(many=True)
# 	return scores_schema.jsonify(scores)

# @blueprint.post('/')
# def create():
# 	name = request.json.get('name', '')
# 	points = session.get('points', 0)

# 	# use webargs
# 	if points >= 50 \
# 		and 3 <= len(name.strip()) <= 8 \
# 		and re.match(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*', name.strip()):
		
# 		score = Score(name=name, points=points)
# 		db.session.add(score)
# 		db.session.commit()

# 	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
# 	scores_schema = ScoreSchema(many=True)
# 	return scores_schema.jsonify(scores)

# ---
# Devlopment version
# 
# Show new entry in leaderboard.
# 
# Problems:
# - is new entry realy visible in table (Yes)
# - how to format high ranking numbers in table


from sqlalchemy import func
from .schemas import RankSchema

@blueprint.route('/test')
def test_index():
	rankings = Score.query.with_entities(
		Score.id, 
		Score.name, 
		Score.points, 
		func.row_number().over(order_by=Score.points.desc()).label('rank'), 
	).order_by(Score.points.desc()).limit(10).all()

	scores_schema = RankSchema(many=True)
	return scores_schema.jsonify(rankings)

@blueprint.post('/test')
def test_create():
	name = request.json.get('name', '')
	points = session.get('points', 0)

	if points >= 50 \
		and 3 <= len(name.strip()) <= 8 \
		and re.match(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*', name.strip()):
		
		score = Score(name=name, points=points)
		db.session.add(score)
		db.session.commit()

	rank_up = Score.query.filter(Score.points >= points).count()
	rank_down = Score.query.filter(Score.points < points).count()
	
	start_rank = max(1, rank_up - (4 if rank_down >= 6 else 9 - rank_down))
	end_rank = start_rank + 9

	ranks = Score.query.with_entities(
		Score.id, 
		Score.name, 
		Score.points, 
		func.row_number().over(order_by=Score.points.desc()).label('rank'), 
	).order_by(Score.points.desc()).slice(start_rank - 1, end_rank).all()

	scores_schema = RankSchema(many=True)
	return scores_schema.jsonify(ranks)
