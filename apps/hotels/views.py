from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler

from tables import BaseModel, UserPofile, Country, session


class IndexHandler(RequestHandler):

    def get(self):
        print(session.query(UserPofile).all())
        if self.get_argument('create_user', False):
            user = UserPofile(first_name=u"Evgeniy", second_name=u"Hacko", middle_name=u"Gennadievich", email="hacko@nicecode.biz")
            user.set_password('password')
            session.add(user)
            try:
                session.commit()
            except Exception, e:
                self.write(u"Exception: %s" % e.message)
                session.rollback()
        self.write("Hotels index view")