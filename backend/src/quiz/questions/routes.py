from .. import db
from .constants import (
	LEVELS, 
	POINTS_PER_QUESTION, 
	QUESTIONS_PER_LEVEL
)
from .models import Hit
from .utils import find_parts
from flask import (
	Blueprint, 
	current_app, 
	jsonify, 
	request, 
	session
)
from sqlalchemy import func # , or_
import random


blueprint = Blueprint(
	'questions',
	__name__,
	url_prefix='/questions'
)

@blueprint.route('/')
def index():
	level = session['level'] = 1
	points = session['points'] = 0

	q = Hit.query\
		.filter( 
			Hit.peak <= LEVELS[level]['peak'], 
			Hit.weeks >= LEVELS[level]['weeks'], 
			Hit.year.in_(range(LEVELS[level]['f_range'],LEVELS[level]['t_range'])), 
			# Hit.id.not_in(session['seen_songs']) # Viewed questions list is empty.
		).order_by(func.random()).limit(1).first()
	session['seen_songs'] = [q.id]

	# What if no question was found? 
	# - No hit available within the level.
	#	-> At least one question is required in level 1.

	# Generate the 4 alternatives including the correct answer
	alternatives = [q.artist]

	# Getting 3 random artists from same level
	fail_count = 0
	while len(alternatives) < 4 and fail_count < 12:
		alt = Hit.query\
			.filter(
				Hit.peak <= LEVELS[level]['peak'], 
				Hit.weeks >= LEVELS[level]['weeks'], 
				# Hit.year.in_(range(LEVELS[level]['f_range'],LEVELS[level]['t_range'])), 
				# Modifying year range so that the alternatives are from same era
				Hit.year.in_(range(q.year-5,q.year+5)), 
				Hit.artist.not_in(alternatives), 
				# Hit.id.not_in(session['seen_songs']) # Why should this limitation exist?
			).order_by(func.random()).limit(1).first()
		if not alt:
			current_app.logger.warning('No suitable answer found in database.')
			break
		if any(find_parts(alt.artist, artist) or find_parts(artist, alt.artist) for artist in alternatives):
			fail_count += 1
			current_app.logger.warning('No suitable answer found. %d attempts left.', 12 - fail_count)
			continue
		alternatives.append(alt.artist)

	# Shuffle the alternatives
	random.shuffle(alternatives)

	# The id of the current question
	session['qid'] = q.id
	# The id of every correct guess
	session['qids'] = [] 
	# Fail counter
	session['fails'] = 0
	# List of 'failed' songs
	session['failed_songs'] = []

	# Building the actual question
	question = f"'{q.song}'"
	question_info = f"#{q.peak} in {q.year}"

	return jsonify(
		level=level,
		points=points,
		question=question,
		question_info=question_info,
		alternatives=alternatives,
		finished=len(alternatives) < 4, 
		lives=3
	)  


@blueprint.post('/')
def update(): 
	level = session.get('level', 1)
	points = session.get('points', 0)
	qid = session.get('qid')

	# Validate given answer
	q = Hit.query.get_or_404(qid)
	if request.json.get('value', '') == q.artist: 
		session['qids'].append(q.id) 
		session.modified = True
		points = session['points'] = (points + level*POINTS_PER_QUESTION)
		if points >= sum(QUESTIONS_PER_LEVEL*x*POINTS_PER_QUESTION for x in range(1, level + 1)): 
			level = session['level'] = level + 1
			# session['qids'] = []

	else:
		session['fails'] += 1 
		session['failed_songs'].append({'artist': q.artist, 'song': q.song})

	# Generate the next question
	# - What if level 21 is reached? (SOLVED)
	#   -> KeyError in LEVELS from quiz_settings.
	level_key = min(level, max(*LEVELS.keys()))

	qs = Hit.query\
		.filter(
			Hit.peak <= LEVELS[level_key]['peak'], 
			Hit.weeks >= LEVELS[level_key]['weeks'], 
			Hit.year.in_(range(LEVELS[level_key]['f_range'],LEVELS[level_key]['t_range'])), 
			Hit.id.not_in(session['seen_songs'])
		).order_by(func.random()).limit(1).first()

	# What if no question was found? (SOLVED)
	# - No hit available within the level.
	#	-> At least 7 questions are required per level.
	#   -> Since level 20 is the last lookup, the problem can occur here.
	# - All Hit already seen.

	if qs: 
		q = qs
		session['seen_songs'].append(q.id)
		session.modified = True

		# Generate the 4 alternatives including the correct answer
		alternatives = [q.artist]

		# Getting 3 random artists from same level
		fail_count = 0
		while len(alternatives) < 4 and fail_count < 12:
			alt = Hit.query\
				.filter(
					Hit.peak <= LEVELS[level_key]['peak'], 
					Hit.weeks >= LEVELS[level_key]['weeks'], 
					# Hit.year.in_(range(LEVELS[level_key]['f_range'],LEVELS[level_key]['t_range'])), 
					# Modifying year range so that the alternatives are from same era
					Hit.year.in_(range(q.year-5,q.year+5)), 
					Hit.artist.not_in(alternatives), 
					# or_(
					# 	or_(*[~Hit.artist.contains(artist) for artist in alternatives]), 
					# 	or_(*[~literal(artist).contains(Hit.artist) for artist in alternatives])
					# )
					# Hit.id.not_in(session['seen_songs']) # Why should this limitation exist?
				).order_by(func.random()).limit(1).first()
			if not alt:
				current_app.logger.warning('No suitable answer found in database.')
				break
			if any(find_parts(alt.artist, artist) or find_parts(artist, alt.artist) for artist in alternatives):
				fail_count += 1
				current_app.logger.warning('No suitable answer found. %d attempts left.', 12 - fail_count)
				continue
			alternatives.append(alt.artist)

		# Shuffle the alternatives
		random.shuffle(alternatives)

		# The id of the current question
		session['qid'] = q.id

		# Building the actual question
		question = f'"{q.song}"'
		question_info = f"#{q.peak} in {q.year}"

	# Check if game is over
	# - When three failed attempts have been achieved.
	# - When the same question is asked again.
	done = session['fails'] >= 3 or q.id in session['qids'] or len(alternatives) < 4

	lives = 3 - int(session.get('fails', 3))

	return jsonify(
		level=level,
		points=points,
		question=question if not done else None,
		question_info=question_info if not done else None,
		alternatives=alternatives if not done else [],
		finished=done, 
		lives=lives,
		failed_songs = session['failed_songs']
	)
