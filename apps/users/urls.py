from .views import IndexHandler, LoginHandler

url_patterns = [
    (r'/users/', IndexHandler),
    (r'/users/login', LoginHandler)
]