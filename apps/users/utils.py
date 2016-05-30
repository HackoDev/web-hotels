from tornado.web import RequestHandler
import hashlib


def make_password(password):
    """ Generate hash password from raw 
    :return: hashed string"""
    return hashlib.sha256(str.encode(password)).hexdigest()


class LoginRequiredMixin(RequestHandler):
    """ Login required mixin """

    def get_current_user(self):
        return self.get_secure_cookie("user")