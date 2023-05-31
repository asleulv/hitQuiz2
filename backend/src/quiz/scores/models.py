from .. import db
from datetime import datetime

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	points = db.Column(db.Integer, nullable=False)

	created_at = db.Column(db.DateTime,
		nullable=False, unique=False, index=False,
		default=datetime.utcnow)