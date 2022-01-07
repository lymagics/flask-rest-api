from rest import Base, Session
from rest.models import User, Address
from rest.views import get_last_id


class TestDatabase:
	"""Class includes tests for database."""
	def __init__(self, session):
		self.session = session()

	def test_insert(self):
		"""INSERT test function."""
		try:
			name = 'Bob'
			city = 'Chicago'
			street = 'Michigan Avenue'

			address = Address(city=city, street=street)
			user = User(name=name, Address=address)

			self.session.add(address)
			self.session.add(user)
			self.session.commit()
			return 'Test insert ended successfully.'
		except:
			return 'Unable to add user. Test insert failed.'

	def test_select(self):
		"""SELECT test function."""
		try:
			last_id = get_last_id()
			user = self.session.query(User).filter(User.id_ == last_id).first()
			address = self.session.query(Address).filter(Address.id_ == user.address_id).first()
			return 'Test select ended successfully.'
		except:
			return 'Unable to get user. Test select failed.'

	def test_update(self):
		"""UPDATE test function."""
		try:
			last_id = get_last_id()
			user = self.session.query(User).filter(User.id_ == last_id).first()
			address = self.session.query(Address).filter(Address.id_ == user.address_id).first()
			user.name = 'Alice'
			address.city = 'NewYork'
			address.street = 'Broadway'
			self.session.commit()
			return 'Test update ended successfully.'
		except:
			return 'Unable to update user. Test update failed.'

	def test_delete(self):
		"""DELETE test function."""
		try:
			last_id = get_last_id()
			user = self.session.query(User).filter(User.id_ == last_id).first()
			address = self.session.query(Address).filter(Address.id_ == user.address_id).first()

			self.session.delete(user)
			self.session.delete(address)
			self.session.commit()
			return 'Test delete ended successfully.'
		except:
			return 'Unable to delete user. Test delete failed.'


if __name__ == '__main__':
	test_database = TestDatabase(Session)
	print(test_database.test_insert())
	print(test_database.test_select())
	print(test_database.test_update())
	print(test_database.test_delete())