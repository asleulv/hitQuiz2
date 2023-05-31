from .. import db

class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    artist = db.Column(db.String(150), index=True)
    song = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    peak = db.Column(db.Integer, index=True)
    weeks = db.Column(db.Integer, index=True)
