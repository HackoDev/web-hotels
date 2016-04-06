from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(__file__)

settings = dict(
    template_path=os.path.join(BASE_DIR, "templates"),
    static_path=os.path.join(BASE_DIR, "static"),
    xsrf_cookie=True,
    cookie_secret='qwdlk;2d1oih9gf31484`23youidglqwe12w1s8tyoi2'
)

engine = create_engine("sqlite:///:memory:", echo=True)