from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import *
import settings
import hashlib

engine = create_engine('sqlite:///' + settings.DB_PATH)
BaseModel = declarative_base()
BaseModel.metadata.bind = engine


# authenticate tables

POSITION_CHOICES = [(str(i), str(i)) for i in range(1, 6)]


class UserProfile(BaseModel):
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

    def make_password(self, password):
        return hashlib.sha256(password).hexdigest()

    def set_password(self, password):
        self.password = self.make_password(password)

    def check_password(self, raw_passord):
        return self.password == self.make_password(raw_passord)

    def __repr__(self):
        return "<User(first_name={first_name}, last_name={second_name}>".format(**dict(
            first_name=self.first_name, second_name=self.second_name))

    def __str__(self):
        return "%s %s" % (self.first_name, self.middle_name)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"


class Country(BaseModel):

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, info={"verbose_name": "Id"})
    title = Column(String(255), nullable=False, default="", info={"verbose_name": "Название"})

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
        )

    def __str__(self):
        return self.title.strip()

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class City(BaseModel):

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    country_id = Column(Integer, ForeignKey(Country.id), nullable=False, info={"verbose_name": "Страна"})
    title = Column(String(255), nullable=False, default="", info={"verbose_name": "Название"})

    def to_dict(self):
        return dict(
            id=self.id,
            country_id=self.country_id,
            title=self.title,
        )

    def country(self):
        return session.query(Country).filter(Country.id == self.country_id).one()

    country.info = {"verbose_name": "Страна"}

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Hotel(BaseModel):

    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    city_id = Column(Integer, ForeignKey(City.id), nullable=False, info={"verbose_name": "Город"})
    title = Column(String(512), default="", nullable=False, info={"verbose_name": "Название"})
    position = Column(Integer, default=3, nullable=False, info={"verbose_name": "Звездность"})

    def city(self):
        return session.query(City).filter(City.id == self.city_id).one()

    city.info = {"verbose_name": "Город"}

    def __str__(self):
        return self.title

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            position=self.position,
        )

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"


class Room(BaseModel):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    title = Column(String(512), default="", nullable=False, info={"verbose_name": "Название"})
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False, info={"verbose_name": "Отель"})
    description = Column(String(1024), default="", nullable=True, info={"verbose_name": "Описание"})

    def __str__(self):
        return self.title

    def hotel(self):
        return session.query(Hotel).filter(Hotel.id == self.hotel_id).one()

    hotel.info = {"verbose_name": "Отель"}

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            hotel_id=self.hotel_id
        )

    def price(self):
        result = session.query(RoomPrice).filter(RoomPrice.room_id == self.id).order_by(RoomPrice.id.desc()).first()
        if result:
            return result.value
        return 0

    def set_price(self, value):
        assert isinstance(value, int) or isinstance(value, float), "Incorrect number value"
        RoomPrice(value=value, room=self.id)

    price.info = {"verbose_name": "Цена"}

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"


class RoomPrice(BaseModel):

    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False, info={"verbose_name": "Номер"})
    value = Column(Float, default=0, nullable=False, info={"verbose_name": "Цена"})

    def to_dict(self):
        return dict(
            id=self.id,
            room_id=self.room_id,
            value=self.value
        )

    def __str__(self):
        return self.title

    def room(self):
        return ": ".join([
            str(session.query(Hotel).join(Room, Room.hotel_id == Hotel.id).filter(Room.id == self.room_id).one()),
            str(session.query(Room).filter(Room.id == self.room_id).one())
        ])

    room.info = {"verbose_name": "Номер"}

    def __str__(self):
        return "%s: %s руб." % (self.room(), self.value)

    class Meta:
        verbose_name = "Цена номера"
        verbose_name_plural = "Цены номеров"


BaseModel.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
