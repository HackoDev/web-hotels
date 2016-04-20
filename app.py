from tornado.options import define, options
from tornado.options import parse_command_line
from tornado import httpserver
from tornado import ioloop
from tornado import web

from apps.main.urls import url_patterns as main_urls
from apps.users.urls import url_patterns as user_urls
from apps.hotels.urls import url_patterns as hotels_urls
from apps.reports.urls import url_patterns as reports_urls
from apps.admin.urls import url_patterns as admin_urls
from settings import settings
import ui_methods


define("port", default=8000, help="run on the given port", type=int)


if __name__ == "__main__":
    print("Run server")
    parse_command_line()
    
    # add url patterns
    handlers = []
    handlers.extend(main_urls)
    handlers.extend(user_urls)
    handlers.extend(hotels_urls)
    handlers.extend(reports_urls)
    handlers.extend(admin_urls)

    # create tornado web app
    app = web.Application(handlers=handlers, ui_methods=ui_methods, autoreload=True, **settings)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
