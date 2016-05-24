from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler
import json

from tables import BaseModel, UserProfile, Country, City, Hotel, session


class HotelSearchListView(RequestHandler):

    def json(self, data_dict):
        self.set_header("Content-Type", 'application/json')
        self.finish(json.dumps(data_dict))

    def get(self):

        country = self.get_argument("country", None)
        city = self.get_argument("city", None)
        title = self.get_argument("title", None)
        position = self.get_argument("position", None)

        query = session.query(Hotel).filter()

        if country is not None:
            query = query.join(City, City.id == Hotel.city_id).join(Country, Country.id == City.country_id).filter(Country.id == country)

        if city is not None:
            query = query.filter(Hotel.city_id == city)

        if title is not None:
            query = query.filter(Hotel.title.like("%" + title + "%"))

        if position is not None:
            query = query.filter(Hotel.position == position)

        self.json([item.to_dict() for item in query])


class RoomSearchListView(RequestHandler):
    pass
        # print(session.query(UserProfile).all())
        # if self.get_argument('create_user', False):
        #     user = UserProfile(first_name="Evgeniy", second_name="Hacko", middle_name="Gennadievich", email="hacko@nicecode.biz")
        #     user.set_password('password')
        #     session.add(user)
        #     try:
        #         session.commit()
        #     except Exception as e:
        #         self.write("Exception: %s" % e.message)
        #         session.rollback()
        # self.write("Hotels index view")