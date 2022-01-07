import unittest
from flask import jsonify
from rest import create_app, Session
from rest.models import User, Address 
from rest.views import get_last_id


class TestApplication(unittest.TestCase):
	"""Class includes tests for application routes."""
	API_URL = 'http://127.0.0.1:5000'

	INDEX_PAGE = f"{API_URL}/"

	app = create_app().test_client()
	session = Session()

	def test_1_post(self):
		"""POST method test."""
		query = {
			'name': 'Bob',
			'city': 'NewYork',
			'street': 'Broadway'
		}
		r = TestApplication.app.post(TestApplication.INDEX_PAGE, json=query)
		self.assertEqual(r.status_code, 201)

	def test_2_get(self):
		"""GET method test."""
		r = TestApplication.app.get(TestApplication.INDEX_PAGE)
		self.assertEqual(r.status_code, 201)

	def test_3_get_one(self):
		"""GET method test."""
		last_id = get_last_id()
		r = TestApplication.app.get(f"{TestApplication.INDEX_PAGE}{last_id}")
		self.assertEqual(r.status_code, 201)

	def test_4_put(self):
		"""PUT method test."""
		query = {
			'name': 'Alice',
			'city': 'Chicago',
			'street': 'Michigan Avenue'
		}
		last_id = get_last_id()
		r = TestApplication.app.put(f"{TestApplication.INDEX_PAGE}{last_id}", json=query)
		self.assertEqual(r.status_code, 201)

	def test_5_delete(self):
		"""DELETE method test."""
		last_id = get_last_id()
		r = TestApplication.app.delete(f"{TestApplication.INDEX_PAGE}{last_id}")
		self.assertEqual(r.status_code, 204)


if __name__ == '__main__':
	unittest.main()