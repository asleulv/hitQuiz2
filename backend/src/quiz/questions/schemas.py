from .. import ma
from .models import Hit

class HitSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Hit