from .. import ma

class RankSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'points', 'rank')
