from .views import HotelListViewView

url_patterns = [
    (r'/hotels/', HotelListViewView)
]