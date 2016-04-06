from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import *


BaseModel = declarative_base()


# authenticate tables


class UserPoile(BaseModel):
	"""
	User models for authenticate and storing information
	"""
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	first_name = Column(String(255), default="")
	second_name = Column(String(255), default="")
	middle_name = Column(String(255), default="")

	# auth info
	email = Column(String(255), nullable=False, unique=True)
	password = Column(String(), nullable=False)

	is_staff = Column(Boolean, default=False)

	def set_password(self, password):
		self.password = password

	def __repr__(self):
		return "<User(first_name={first_name}, last_name={second_name}>".format(**dict(
			first_name=self.first_name, second_name=self.second_name))

	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.middle_name)



class 
engine = create_engine('sqlite:///db.sqlite')
BaseModel.metadata.create_all(engine)
