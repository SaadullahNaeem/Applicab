from channels.routing import route_class, include
from .consumers import *

from channels.staticfiles import StaticFilesConsumer


http_routing = {
    'http.request': StaticFilesConsumer()
}

channel_routing = [
    route_class(BookingConsumer, path=r"^/booking."),
    include(http_routing)
]
