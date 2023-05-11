from app import db

class Hits(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    artist = db.Column(db.String(150), index=True)
    song = db.Column(db.String(150), index=True)
    year = db.Column(db.String(4), index=True)
    peak = db.Column(db.String(3), index=True)
    weeks = db.Column(db.String(3), index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'song': self.song,
            'year': self.year,
            'peak': self.peak,
            'weeks': self.weeks
        }

    def __repr__(self):
        return '<Hit: {}>'.format(self.song)