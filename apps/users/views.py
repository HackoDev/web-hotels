from tornado.web import RequestHandler
from .forms import AuthForm


class IndexHandler(RequestHandler):

    def get(self):
        self.write("Users inde view")


class LoginHandler(RequestHandler):

    def post(self):
        form = AuthForm(self.request.arguments)
        if form.validate():
            self.set_secure_cookie("user", form.data)
            self.redirect(self.reverse_url("admin:index"))
        raise ValueError(form.errors)
        self.get()

    def get(self):
        kwargs = {
            "auth_form": AuthForm()
        }
        self.render("login.html", **kwargs)
