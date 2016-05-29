from tornado.web import RequestHandler


class IndexHandler(RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.render("app.html", user=self.get_current_user())
