from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler
import datetime
import json

from tables import BaseModel, UserProfile, Country, City, Hotel, Room, Reservation, session


class BaseJSONMixin(RequestHandler):
    
    def json(self, data_dict):
        self.set_header("Content-Type", 'application/json')
        self.finish(json.dumps(data_dict))


class HotelSearchListView(BaseJSONMixin):

    def get(self):

        country = self.get_argument("country", None)
        city = self.get_argument("city", None)
        title = self.get_argument("title", None)
        position = self.get_argument("position", None)

        query = session.query(Hotel).filter()

        if country is not None and country:
            query = query.join(City, City.id == Hotel.city_id).join(Country, Country.id == City.country_id).filter(Country.id == country)

        if city is not None and city:
            query = query.filter(Hotel.city_id == city)

        if title is not None and title:
            query = query.filter(Hotel.title.like("%" + title + "%"))

        if position is not None and position:
            query = query.filter(Hotel.position == position)

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
        start_date = self.get_argument("start_date", None)
        end_date = self.get_argument("end_date", None)
        try:
            room = session.query(Room).filter(Room.id == int(room_id)).one()
        except:
            self.set_status(404)
            self.finish("not found")
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except:
            self.set_status(400)
            self.finish({"details": "Некорректная дата"})

        s_date, e_date = room.is_busy()

        if s_date is e_date is None:
            self.set_status(400)
            self.json({"details": "Номер занят"})
        self.json({"details": "Квартира свободна"})


class RoomSearchListView(BaseJSONMixin):

    def get(self):

        query = session.query(Room).filter()
        hotel = self.get_argument("hotel", None)
        if hotel is not None:
            query = query.filter(Room.hotel_id == int(hotel))
        return self.json([item.to_dict() for item in query])
