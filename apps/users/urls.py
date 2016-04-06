from .views import IndexHandler

url_patterns = [
	(r'/users/', IndexHandler)
]