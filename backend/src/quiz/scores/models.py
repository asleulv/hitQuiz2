from .. import db

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	points = db.Column(db.Integer, nullable=False)
