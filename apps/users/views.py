from tornado.web import RequestHandler
from .forms import AuthForm
from .utils import LoginRequiredMixin


class IndexHandler(RequestHandler):

    def get(self):
        self.write("Users inde view")


class LoginHandler(LoginRequiredMixin):

    def post(self):
        form = AuthForm(self.request.arguments)
        if form.validate():
            self.clear_cookie("user")
            self.set_secure_cookie("user", str(form.data.id))
            self.redirect(self.reverse_url("admin:index"))
        self.get()

    def get(self):
        kwargs = {
            "auth_form": AuthForm()
        }
        self.render("login.html", **kwargs)
