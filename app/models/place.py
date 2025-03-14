from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
	def __init__(self, title, description, price, latitude, longitude, owner):
		super().__init__()
		self.title = title[:100]
		self.description = description
		self.price = max(0, float(price))
		self.latitude = min(max(float(latitude), -90.0), 90.0)
		self.longitude = min(max(float(longitude), -180.0), 180.0)
		if isinstance(owner, User):
			self.owner = owner
		else:
			raise ValueError('Owner must be a valid user instance')
		self.reviews = []
		self.amenities = []

	def add_review(self, review):
		if review not in self.reviews:
			self.reviews.append(review)

	def add_amenity(self, amenity):
		if amenity not in self.amenities:
			self.amenities.append(amenity)
