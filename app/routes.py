from app import app, db
from flask import render_template, redirect, request, url_for, session, jsonify, send_from_directory
from app.models import Hits
import random
from sqlalchemy.sql.expression import func, select
from app.quiz_settings import levels

@app.route('/quiz')
def quiz():
	level = session['level'] = 1
	points = session['points'] = 0

	q = Hits.query\
		.filter( 
			Hits.peak <= levels[level]['peak'], 
			Hits.weeks > levels[level]['weeks'], 
			Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range'])), 
			# Hits.id.not_in(session['seen_songs']) # Viewed questions list is empty.
		).order_by(func.random()).limit(1).first()
	session['seen_songs'] = [q.id]

	# What if no question was found? 
	# - No hit available within the level.
	#	-> At least one question is required in level 1.

	# Generate the 4 alternatives including the correct answer
	alternatives = [q.artist]

	# Getting 3 random artists from same level
	while len(alternatives) < 4:
		alt = Hits.query\
			.filter(
				Hits.peak == levels[level]['peak'], 
				Hits.weeks > levels[level]['weeks'], 
				Hits.year.in_(range(levels[level]['f_range'],levels[level]['t_range'])), 
				Hits.artist.not_in(alternatives), 
				# Hits.id.not_in(session['seen_songs']) # Why should this limitation exist?
			).order_by(func.random()).limit(1).first()
		alternatives.append(alt.artist)

	# Shuffle the alternatives
	random.shuffle(alternatives)

	# The id of the current question
	session['qid'] = q.id
	# The id of every correct guess
	session['qids'] = [] 
	# Fail counter
	session['fails'] = 0

	# Building the actual question + question info (peak+year)
	question = f"'{q.song}'"
	question_info = f"#{q.peak} in {q.year}"

	return jsonify(
		level=level,
		points=points,
		question=question,
		question_info=question_info,
		alternatives=alternatives,
		finished=False
	)  


@app.post('/quiz')
def quiz_solve():
	level = session.get('level', 1)
	points = session.get('points', 0)
	qid = session.get('qid')
	
	# Validate given answer
	q = Hits.query.get_or_404(qid)
	if request.json.get('value', '') == q.artist: 
		session['qids'].append(q.id) 
		points = session['points'] = (points + 10) 
		if points >= level*50:
			level = session['level'] = level + 1
			session['qids'] = []

	else:
		session['fails'] += 1 

	# Generate the next question
	# - What if level 5 is reached? (SOLVED)
	#   -> KeyError in levels from quiz_settings.
	level_key = min(level, max(*levels.keys()))

	qs = Hits.query\
		.filter(
			Hits.peak == levels[level_key]['peak'], 
			Hits.weeks > levels[level_key]['weeks'], 
			Hits.year.in_(range(levels[level_key]['f_range'],levels[level_key]['t_range'])), 
			Hits.id.not_in(session['seen_songs'])
		).order_by(func.random()).limit(1).first()

	# What if no question was found? (SOLVED)
	# - No hit available within the level.
	#	-> At least 8 questions are required per level.
	#   -> Since level 4 is the last lookup, the problem can occur here.
	# - All hits already seen.

	if qs: 
		q = qs
		session['seen_songs'].append(q.id)
		session.modified = True

		# Generate the 4 alternatives including the correct answer
		alternatives = [q.artist]

		# Getting 3 random artists from same level
		while len(alternatives) < 4:
			alt = Hits.query\
				.filter(
					Hits.peak == levels[level_key]['peak'], 
					Hits.weeks > levels[level_key]['weeks'], 
					Hits.year.in_(range(levels[level_key]['f_range'],levels[level_key]['t_range'])), 
					Hits.artist.not_in(alternatives), 
					# Hits.id.not_in(session['seen_songs']) # Why should this limitation exist?
				).order_by(func.random()).limit(1).first()
			alternatives.append(alt.artist)

		# Shuffle the alternatives
		random.shuffle(alternatives)
	
		# The id of the current question
		session['qid'] = q.id

		# Building the actual question + question info (peak+year)
		question = f"'{q.song}'"
		question_info = f"#{q.peak} in {q.year}"

	# Check if game is over
	# - When three failed attempts have been achieved.
	# - When the same question is asked again.
	done = session['fails'] >= 3 or q.id in session['qids']

	return jsonify(
		level=level,
		points=points,
		question=question if not done else None,
		question_info=question_info if not done else None,
		alternatives=alternatives if not done else [],
		finished=done
	)
