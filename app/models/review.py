from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text
		self.rating = max(1, min(int(rating), 5))
		if isinstance(place, Place):
			self.place = place
		else:
			raise ValueError('Place must be a valid Place instance')
		if isinstance(user, User):
			self.user = user
		else:
			raise ValueError('User must be a valid User instance')
