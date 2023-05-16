from .. import ma
from .models import Score
from marshmallow import validate

class ScoreSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Score
	
	name = ma.String(required=True, 
		# currently unused
		validate=[
			validate.Length(min=2, max=8), 
			validate.Regexp(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*$'), 
		]
	)
	
	points = ma.Integer(required=False)
