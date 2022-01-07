from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from . import Base


class User(Base):
	"""A database table to represent user.
	
	id_ int User identificator in database.
	name string User name.

	address_id int Reference on user address in address table.
	"""
	__tablename__ = 'user'

	id_ = Column(Integer(), primary_key=True)
	name = Column(String(30), nullable=False)

	address_id = Column(Integer(), ForeignKey('address.id_'))
	Address = relationship('Address')

	def __repr__(self):
		return f'<User: {self.name}>'


class Address(Base):
	"""A database table to represent user's address.

	id_ int Address identificator in database.
	city string A city where user lives.
	street string A street where user lives.
	"""
	__tablename__ = 'address'

	id_ = Column(Integer(), primary_key=True)
	city = Column(String(20), nullable=False)
	street = Column(String(30), nullable=False)

	User = relationship('User')

	def __repr__(self):
		return f'<City {self.city} Street {self.street}>'