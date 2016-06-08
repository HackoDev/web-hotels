from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler
from tornado.escape import json_decode
import datetime
import json

from tables import BaseModel, UserProfile, Country, City, Hotel, Room, Reservation, session, RoomPrice
from apps.hotels.forms import UserReservationForm
from . import utils


class BaseJSONMixin(RequestHandler):
    
    def json(self, data_dict):
        self.set_header("Content-Type", 'application/json')
        self.finish(json.dumps(data_dict))


class HotelSearchListView(BaseJSONMixin):

    def get(self):

        country = utils.get_int_or_none(self.get_argument("country", None))
        city = utils.get_int_or_none(self.get_argument("city", None))
        position = utils.get_int_or_none(self.get_argument("position", None))
        min_price = utils.get_float_or_none(self.get_argument("min_price", None))
        max_price = utils.get_float_or_none(self.get_argument("max_price", None))
        title = self.get_argument("title", None)

        query = session.query(Hotel).filter()

        if country is not None and country > 0:
            query = query.join(City, City.id == Hotel.city_id).join(Country, Country.id == City.country_id).filter(Country.id == country)

        if city is not None and city:
            query = query.filter(Hotel.city_id == city)

        if title is not None and title:
            query = query.filter(Hotel.title.like("%" + title + "%"))

        if position is not None and position:
            query = query.filter(Hotel.position == position)

        if min_price and min_price > 0:
            query = query.join(Room, Room.hotel_id == Hotel.id).join(RoomPrice, RoomPrice.room_id == Room.id)\
                .filter(RoomPrice.value >= min_price)

        if max_price and max_price > min_price and max_price > 0:
            query = query.join(Room, Room.hotel_id == Hotel.id).join(RoomPrice, RoomPrice.room_id == Room.id)\
                .filter(RoomPrice.value <= max_price)

        hotels = []
        for item in query:
            data_dict = item.to_dict()
            city = item.city()
            data_dict.update({
                "city": city.to_dict(),
                "country": city.country().to_dict()
            })
            hotels.append(data_dict)
        self.json(hotels)


class HotelDetailsView(BaseJSONMixin):

    def get(self, hotel_id):

        try:
            hotel = session.query(Hotel).filter(Hotel.id == int(hotel_id)).one()
        except:
            self.set_status(400)
            self.json({"details": "Not found"})
        data_dict = hotel.to_dict()
        city = hotel.city()
        data_dict.update({
            "city": city.to_dict(),
            "country": city.country().to_dict(),
            "rooms": [room.to_dict() for room in hotel.get_rooms()]
        })
        self.json(data_dict)


class ReservationSetView(BaseJSONMixin):

    def post(self, room_id):
        try:
            data_dict = json_decode(self.request.body)
        except Exception as e:
            self.set_status(400)
            self.json({"details": "Некорректные данные"})
        form = UserReservationForm(data=data_dict)
        if not form.validate():
            self.set_status(400)
            self.json({"details": "Некорректные данные", "error": form.errors})
            return
        print(form.data)
        try:
            room = session.query(Room).filter(Room.id == int(room_id)).one()
        except:
            self.set_status(404)
            self.finish("not found")
            return
        try:
            start_date = datetime.datetime.strptime(form.data['start_date_time'], "%Y-%m-%d")
            end_date = datetime.datetime.strptime(form.data["end_date_time"], "%Y-%m-%d")
        except:
            self.set_status(400)
            self.finish({"details": "Некорректная дата"})
            return
        else:

            s_date, e_date = room.is_busy(start_date, end_date)

            if s_date is None:
                data = form.data.copy()
                data.update({
                    "start_date_time": start_date,
                    "end_date_time": end_date,
                    "room_id": int(room_id),
                    "price": room.price()
                })
                reservation = Reservation(**data)
                session.add(reservation)
                try:
                    session.commit()
                except:
                    session.rollback()
                self.json({"details": "Номер свободен"})
                return
            self.set_status(400)
            self.json({"details": "Номер занят"})


class RoomSearchListView(BaseJSONMixin):

    def get(self):

        query = session.query(Room).filter()
        hotel = self.get_argument("hotel", None)
        if hotel is not None:
            query = query.filter(Room.hotel_id == int(hotel))
        return self.json([item.to_dict() for item in query])


class CountriesListView(BaseJSONMixin):

    def get(self):
        self.json([country.to_dict() for country in session.query(Country).all()])


class CitiesListView(BaseJSONMixin):

    def get(self):
        self.json([country.to_dict() for country in session.query(City).all()])
