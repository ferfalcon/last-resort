from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
	def __init__(self):
		self.user_repo = InMemoryRepository()
		self.amenity_repo = InMemoryRepository()
		self.place_repo = InMemoryRepository()
		self.review_repo = InMemoryRepository()

	''' USER '''
	def create_user(self, user_data):
		user = User(**user_data)
		self.user_repo.add(user)
		return user
	
	def get_user(self, user_id):
		return self.user_repo.get(user_id)

	def get_user_by_email(self, email):
		return self.user_repo.get_by_attribute('email', email)
	
	def get_all_users(self):
		return self.user_repo.get_all()
	
	def update_user(self, user_id, user_data):
		user = self.user_repo.get(user_id)
		if not user:
			return None
		user.update(user_data)
		return user

	''' AMENITY '''
	def create_amenity(self, amenity_data):
		amenity = Amenity(**amenity_data)
		self.amenity_repo.add(amenity)
		return amenity
	
	def get_amenity(self, amenity_id):
		return self.amenity_repo.get(amenity_id)
	
	def get_all_amenities(self):
		return self.amenity_repo.get_all()

	def update_amenity(self, amenity_id, amenity_data):
		amenity = self.amenity_repo.get(amenity_id)
		if not amenity:
			return None
		amenity.update(amenity_data)
		return amenity

	''' PLACE '''
	def create_place(self, place_data):
		owner = self.user_repo.get(place_data['owner_id'])
		if not owner:
			return None, 'Owner not found'

		amenities = [self.amenity_repo.get(a_id) for a_id in place_data['amenities']]
		if None in amenities:
			return None, 'One or more amenities not found'

		place = Place(
			title=place_data['title'],
			description=place_data.get('description', ''),
			price=place_data['price'],
			latitude=place_data['latitude'],
			longitude=place_data['longitude'],
			owner=owner,
		)
		for amenity in amenities:
			place.add_amenity(amenity)

		self.place_repo.add(place)
		return place, None

	def get_place(self, place_id):
		return self.place_repo.get(place_id)

	def get_all_places(self):
		return self.place_repo.get_all()
	
	def update_place(self, place_id, place_data):
		place = self.place_repo.get(place_id)
		if not place:
			return None
		place.update(place_data)
		return place
