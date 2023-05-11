from app import app, db
from flask import render_template, redirect, request, url_for, session, jsonify
from app.models import Hits
import random
from sqlalchemy.sql.expression import func, select
from app.quiz_settings import levels


@app.route('/')
@app.route('/quiz')
def quiz():
	session.modified = True
	level = session['lvl'] = 1
	points = session['points'] = 0

	if 'seen_songs' not in session:
		session['seen_songs'] = []   

	while True:      
		q = Hits.query.filter(Hits.peak == levels[level]['peak'], Hits.weeks > levels[level]['weeks'], Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range']))).order_by(func.random()).limit(1).first()
		if q.id not in session['seen_songs']:
			session['seen_songs'].append(q.id)
			break
		else:
			# The song has already been seen, so continue the loop to try again
			continue

	# Generate the 4 alternatives including the correct answer
	alternatives = [q.artist]

	# Building the actual question
	question = f"{q.song} - {q.year}"

	# Getting 3 random artists from same level
	while len(alternatives) < 4:
		alt = Hits.query.filter(Hits.peak == levels[level]['peak'], Hits.weeks > levels[level]['weeks'], Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range']))).order_by(func.random()).limit(1).first()
		if alt.artist in alternatives:
			continue
		if alt.id in session['seen_songs']:
			continue
		alternatives.append(alt.artist)
	
	# The id of the current question
	session['qid'] = q.id
	# The id of every correct guess
	session['qids'] = []
	# Fail counter
	session['fails'] = 0

	# Shuffle the alternatives
	random.shuffle(alternatives)

	return jsonify(level=level,
				   points=points,
				   question=question,
				   alternatives=alternatives,
				   finished=False
				   )  

@app.post('/quiz')
def quiz_solve():
	level = session.get('level', 1)
	points = session.get('points', 0)
	qid = session.get('qid')
	
	# q = Quest.query.get_or_404(qid)
	q = db.get_or_404(Hits, qid)

	if int(request.json.get('value', 0)) == q.artist: 
		session['qids'].append(q.id)
		points = session['points'] = (points + 10) 
		if points >= level*50:
			level = session['level'] = level + 1
			session['qids'] = []

	else:
		session['fails'] += 1 

	# Generate the next question
	while True:      
		q = Hits.query.filter(Hits.peak == levels[level]['peak'], Hits.weeks > levels[level]['weeks'], Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range']))).order_by(func.random()).limit(1).first()
		if q.id not in session['seen_songs']:
			session['seen_songs'].append(q.id)
			break
		else:
			# The song has already been seen, so continue the loop to try again
			continue

	# Generate the 4 alternatives including the correct answer
	alternatives = [q.artist]

	# Building the actual question
	question = f"{q.song} - {q.year}"

	# Getting 3 random artists from same level
	while len(alternatives) < 4:
		alt = Hits.query.filter(Hits.peak == levels[level]['peak'], Hits.weeks > levels[level]['weeks'], Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range']))).order_by(func.random()).limit(1).first()
		if alt.artist in alternatives:
			continue
		if alt.id in session['seen_songs']:
			continue
		alternatives.append(alt.artist)
	
	# The id of the current question
	session['qid'] = q.id

	# Shuffle the alternatives
	random.shuffle(alternatives)

	# Check if game is over
	done = session['fails'] >= 3 or q.id in session['qids']

	return jsonify(level=level,
				   points=points,
				   question=question,
				   alternatives=alternatives,
				   finished=done
				   )