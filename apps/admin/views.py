from tornado.web import RequestHandler


class CountryAdminListView(RequestHandler):

    def get(self, *args, **kwargs):
        self.render("countries.html")
