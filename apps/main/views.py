from tornado.web import RequestHandler
from apps.users.utils import LoginRequiredMixin


class IndexHandler(LoginRequiredMixin):

    def get(self):
        self.render("app.html", user=self.get_current_user())
