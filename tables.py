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


class Country(BaseModel):

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, default="")

    def __unicode__(self):
        return self.title


class City(BaseModel):

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey(Country.id), nullable=False)
    title = Column(String(255), nullable=False, default="")


class Hotel(BaseModel):

    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    title = Column(String(512), default="", nullable=False)
    position = Column(Integer, default=3, nullable=False)


class Room(BaseModel):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False)

    def __get_price(self):
        pass

    def __set_price(self, value):
        assert isinstance(value, int) or isinstance(value, float), "Incorrect number value"
        RoomPrice(value=value, room=self.id)

    property(__get_price, __set_price)


class RoomPrice(BaseModel):

    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    value = Column(Float, default=0, nullable=False)


engine = create_engine('sqlite:///db.sqlite')
BaseModel.metadata.create_all(engine)
