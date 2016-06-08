from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(__file__)

root = lambda *x: os.path.join(BASE_DIR, *x)

DB_SETTINGS = {
	"USER": "root",
	"PASSWORD": "pass",
	"NAME": "booking_db",
	"HOST": "localhost",
	"PORT": "3306"
}
DB_PATH = "booking_db"

settings = dict(
    template_path=root("templates"),
    static_path=root("static"),
    xsrf_cookie=True,
    cookie_secret='qwdlk;2d1oih9gf31484`23youidglqwe12w1s8tyoi2',
    login_url='/users/login'
)
