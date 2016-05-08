from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler

from tables import BaseModel, UserProfile, Country, session


class IndexHandler(RequestHandler):

    def get(self):
        print(session.query(UserProfile).all())
        if self.get_argument('create_user', False):
            user = UserProfile(first_name=u"Evgeniy", second_name=u"Hacko", middle_name=u"Gennadievich", email="hacko@nicecode.biz")
            user.set_password('password')
            session.add(user)
            try:
                session.commit()
            except Exception, e:
                self.write(u"Exception: %s" % e.message)
                session.rollback()
        self.write("Hotels index view")