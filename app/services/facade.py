from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
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

	''' REVIEW '''
	def create_review(self, review_data):
		user = self.user_repo.get(review_data["user_id"])
		if not user:
			return None, "User not found"

		place = self.place_repo.get(review_data["place_id"])
		if not place:
			return None, "Place not found"

		if not (1 <= review_data["rating"] <= 5):
			return None, "Rating must be between 1 and 5"

		review = Review(
			text=review_data["text"],
			rating=review_data["rating"],
			user=user,
			place=place
		)

		self.review_repo.add(review)
		place.add_review(review)
		return review, None

	def get_review(self, review_id):
		return self.review_repo.get(review_id)

	def get_all_reviews(self):
		return self.review_repo.get_all()

	def get_reviews_by_place(self, place_id):
		place = self.place_repo.get(place_id)
		if not place:
			return None, "Place not found"
		return place.reviews, None

	def update_review(self, review_id, review_data):
		review = self.review_repo.get(review_id)
		if not review:
			return None, "Review not found"
		review.update(review_data)
		return review, None

	def delete_review(self, review_id):
		review = self.review_repo.get(review_id)
		if not review:
			return False, "Review not found"

		self.review_repo.delete(review_id)
		review.place.reviews.remove(review)
		return True, None