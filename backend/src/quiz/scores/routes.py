from .. import db
from ..questions.models import Hit
from ..questions.schemas import HitSchema
from .models import Score
from .schemas import RankSchema
from flask import (
	Blueprint, 
	jsonify, 
	request, 
	session, 
	url_for
)
from sqlalchemy import func
import re


blueprint = Blueprint(
	'scores',
	__name__,
	url_prefix='/scores'
)

from datetime import date

@blueprint.route('/')
def index():
	page = request.args.get('page', 0, type=int)
	per_page = request.args.get('per_page', 10, type=int)
	dt = request.args.get('d', None, type=date.fromisoformat)

	query = Score.query.with_entities(
		Score.id, 
		Score.name, 
		Score.points, 
		func.row_number().over(order_by=Score.points.desc()).label('rank'), 
	)

	if dt: 
		query = query.filter(func.date(Score.created_at) == dt)

	ranks = query.order_by(Score.points.desc()).limit(per_page).offset(page*per_page).all()
	
	meta = {}
	if len(ranks) == per_page: 
		meta['next'] = url_for('.index', page=page+1, per_page=per_page, d=dt)

	scores_schema = RankSchema(many=True)
	return jsonify(
		data=scores_schema.dump(ranks), 
		meta=meta 
	)

@blueprint.post('/')
def create():
	name = request.json.get('name', '').strip()
	points = session.get('points', 0)

	score = None
	if points >= 100 \
		and 2 <= len(name) <= 20 \
		and re.match(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*', name): # $ missing but eliminates important characters.
		
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

	meta = {}
	if score:
		meta['current_id'] = score.id

	scores_schema = RankSchema(many=True)
	return jsonify(
		data=scores_schema.dump(ranks), 
		meta=meta
	)

# ---

@blueprint.route('/stats')
def stats():
	seen_songs = session.get('seen_songs', [])
	qids = session.get('fids', [])

	d = []
	l = []
	i = 0
	for song_id in seen_songs[:-1]:
		if song_id not in qids: # answered
			i += 1
			l += [1]
		else: # failed
			l += [2]
		if i == 5:
			d.append(l + [3 for _ in range(7 - len(l))])
			l = []
			i = 0
	d.append(l + [3 for _ in range(7 - len(l))])

	# failed_hit_ids = list(set(session['seen_songs']) - set(session['qids']) - set([session['qid']]))
	failed_hit_ids = session['fids']
	# failed_hits = Hit.query.filter(Hit.id.in_(failed_hit_ids)).all()
	failed_hits = [Hit.query.get(id) for id in reversed(failed_hit_ids)]
	hits_schema = HitSchema(many=True)
	hits_data = hits_schema.dump(failed_hits)

	return jsonify(
		fail_data=d, 
		fail_songs=hits_data
	)

