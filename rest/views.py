from flask import Blueprint, request, jsonify
from . import Session
from .models import User, Address


views = Blueprint('views', __name__)
URL = '/'


def create_session():
	"""Create session with database."""
	return Session()


def get_last_id():
	"""Get last id from database. If database if empty - return 1."""
	try:
		session = Session()
		return session.query(User).all()[-1].id_
	except:
		return 1


def to_dict(name, city, street):
	"""Create dict from name, city and street."""
	return {
		'name': name,
		'city': city,
		'street': street,
	}


def page_not_found(id_):
	user = create_session().query(User).filter(User.id_ == id_).first()
	if not user:
		return True
	return False


@views.route(URL, methods=['POST'])
def post():
	"""POST method route handler."""
	name = request.json.get('name', '')
	city = request.json.get('city', '')
	street = request.json.get('street', '')

	try:
		session = create_session()
		address = Address(city=city, street=street)
		user = User(name=name, Address=address)

		session.add(address)
		session.add(user)
		session.commit()

		return jsonify(to_dict(name, city, street)), 201
	except:
		return jsonify({'error': 'Failed to add info.'}), 400


@views.route(URL, methods=['GET'])
def get():
	"""GET method route handler."""
	try:
		session = create_session()
		users = session.query(User).all()
		address = session.query(Address).all()

		return {'users': [to_dict(users[i].name, address[i].city, address[i].street) for i in range(len(users))]}, 201
	except:
		return jsonify({'error': 'Failed to get info.'}), 404


@views.route(f"{URL}/<id_>", methods=['GET'])
def get_id(id_):
	"""GET method route handler."""
	if page_not_found(id_):
		return "Page not found.", 404

	try:
		session = create_session()
		user = session.query(User).filter(User.id_ == id_).first()
		address = session.query(Address).filter(Address.id_ == user.address_id).first()

		return jsonify(to_dict(user.name, address.city, address.street)), 201
	except:
		return jsonify({'error': 'Failed to get info.'}), 404


@views.route(f"{URL}/<id_>", methods=['PUT'])
def put(id_):
	"""PUT method route handler."""
	name = request.json.get('name', '')
	city = request.json.get('city', '')
	street = request.json.get('street', '')
	if page_not_found(id_):
		return "Page not found.", 404

	try:
		session = create_session()
		user = session.query(User).filter(User.id_ == id_).first()
		address = session.query(Address).filter(Address.id_ == user.address_id).first()

		user.name = name
		address.city = city
		address.street = street

		session.commit()

		return jsonify(to_dict(user.name, address.city, address.street)), 201
	except:
		return jsonify({'error': 'Failed to update info.'}), 400 


@views.route(f"{URL}/<id_>", methods=['DELETE'])
def delete(id_):
	"""DELETE method route handler."""
	if page_not_found(id_):
		return "Page not found.", 404

	try:
		session = create_session()

		user_to_delete = session.query(User).filter(User.id_ == id_).first()
		address = session.query(Address).filter(Address.id_ == user_to_delete.address_id).first()

		response = to_dict(user_to_delete.name, address.city, address.street)

		session.delete(user_to_delete)
		session.delete(address)
		
		session.commit()

		return jsonify(response), 204
	except:
		return jsonify({'error': 'Failed to delete info.'}), 400 