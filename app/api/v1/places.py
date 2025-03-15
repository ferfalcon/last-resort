from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
	'id': fields.String(description='Amenity ID'),
	'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
	'id': fields.String(description='User ID'),
	'first_name': fields.String(description='First name of the owner'),
	'last_name': fields.String(description='Last name of the owner'),
	'email': fields.String(description='Email of the owner'),
})

place_model = api.model('Place', {
	'title': fields.String(required=True, description='Title of the place'),
	'description': fields.String(required=True, description='Description of the place'),
	'price': fields.Float(required=True, description='Price per night'),
	'latitude': fields.Float(required=True, description='Latitude of the place'),
	'longitude': fields.Float(required=True, description='Longitude of the place'),
	'owner_id': fields.String(required=True, description='ID of the owner'),
	'amenities': fields.List(fields.String, required=True, description='List of amenities ID\'s'),
})

@api.route('/')
class PlaceList(Resource):
	@api.expect(place_model, validate=True)
	@api.response(201, 'Place succesfully created')
	@api.response(400, 'Invalid input data')
	@api.response(404, 'Owner or amenities not found')
	def post(self):
		place_data = api.payload
		new_place, error = facade.create_place(place_data)
		if error:
			return {'error': error}, 404
		
		return {
			'id': new_place.id,
			'title': new_place.title,
			'description': new_place.description,
			'price': new_place.price,
			'latitude': new_place.latitude,
			'longitude': new_place.longitude,
			'owner_id': new_place.owner.id,
			'amenities': [a.id for a in new_place.amenities],
		}, 201
	
	@api.response(200, 'List of places retrieved successfully')
	def get(self):
		places = facade.get_all_places()
		return [{
			'id': place.id,
			'title': place.title,
			'latitude': place.latitude,
			'longitude': place.longitude,
		} for place in places], 200
	
@api.route('/<place_id>')
class PlaceResource(Resource):
	@api.response(201, 'Place succesfully created')
	@api.response(400, 'Invalid input data')
	def get(self, place_id):
		place = facade.get_place(place_id)
		if not place:
			return {'error': 'Place not found'}, 404
		return {
			'id': place.id,
			'title': place.title,
			'description': place.description,
			'latitude': place.latitude,
			'longitude': place.longitude,
			'owner': {
				'id': place.owner.id,
				'first_name': place.owner.first_name,
				'last_name': place.owner.last_name,
				'email': place.owner.email,
			},
			'amenities': [{ 'id': a.id,	'name': a.name} for a in place.amenities]
		}, 200

	@api.expect(place_model, validate=True)
	@api.response(200, 'Place updated successfully')
	@api.response(404, 'Place not found')
	@api.response(400, 'Invalid input data')
	def put(self, place_id):
		place_data = api.payload
		updated_place = facade.update_place(place_id, place_data)

		if not updated_place:
			return {'error': 'Place not found'}, 404

		return {
			'id': updated_place.id,
			'title': updated_place.title,
			'description': updated_place.description,
			'price': updated_place.price,
		}, 200