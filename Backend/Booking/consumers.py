from channels.generic import websockets
from .models import *
from Driver.models import Driver
from geopy.distance import great_circle
import pyrebase
import json

config = {
    "apiKey": "AIzaSyA2-fkz-Acck6d8AqSkJjbBM1BQtK2NdtE",
    "authDomain": "cabs-cc162.firebaseapp.com",
    "databaseURL": "https://cabs-cc162.firebaseio.com",
    "projectId": "cabs-cc162",
    "storageBucket": "cabs-cc162.appspot.com",
    "messagingSenderId": "274763249211"
}
firebase = pyrebase.initialize_app(config)


class BookingConsumer(websockets.JsonWebsocketConsumer):
    strict_ordering = True
    channel_session = True
    my_stream = None
    db = firebase.database()

    def connect(self, message, **kwargs):
        try:
            prefix, label = message.content['path'].strip('/').split('/')
            message.channel_session['keys'] = label
        except ValueError:
            pass
        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        if content['action'] == 'create':
            self.createBookingInstance(content['data'])
        elif content['action'] == 'bookings':
            self.getAllBookingInstances(content['data'])
        elif content['action'] == 'getBooking':
            self.getBookingInstance(content['data'])
        elif content['action'] == 'expired':
            self.expiredBookingInstances(content['data'])
        elif content['action'] == 'select':
            self.selectBookingInstance(content['data'])

    def disconnect(self, message, **kwargs):
        if self.my_stream:
            self.my_stream.close()

    def stream_handler(self, message):
        data = message["data"]
        if data:
            paths = []
            paths = message['path'].strip('/').split('/')

            if len(paths) == 2:
                if paths[0] == 'drivers':
                    uid = data['driver']
                    bid = data['BookingId']

                    if Booking.objects.filter(id=bid).exists():
                        booking = Booking.objects.get(id=bid)

                        if Driver.objects.filter(firebaseId__iexact=uid).exists():
                            driver = Driver.objects.get(firebaseId__iexact=uid)
                            mybid = self.createBidInstance(driver, booking, data['quote'])
                            try:
                                location = self.db.child("drivers").child(data['driver']).child('location').get()
                                payload = {'action': 'quote', 'quote': data['quote'], 'location': location.val(),
                                           'booking': mybid, 'taxi': driver.category}
                                self.send(payload)
                            except ValueError:
                                pass

    def createBidInstance(self, driver, booking, quote):
        if not Bids.objects.filter(booking=booking, driver=driver).exists():
            try:
                mybid = Bids.objects.create(driver=driver, booking=booking, quote=quote)
                return mybid.id
            except ValueError:
                pass

    def createBookingInstance(self, content):
        try:
            if len(content['key']) == 5:
                if Booking.objects.filter(client_key=content['key']).exists():
                    books = Booking.objects.filter(client_key=content['key'])
                    for book in books:
                        book.delete()

            booking = Booking.objects.create(client_key=content['key'], pickup=content['pickup'],
                                             destination=content['destination'], level='Waiting')
            drivers = Driver.objects.all()
            for driver in drivers:
                if driver.country == content['country']:
                    if driver.admin_area_1 == content['area1'] and (
                                    driver.admin_area_2 == content['area2'] or driver.admin_area_2 == 'undefined'):
                        newport_ri = (driver.latitude, driver.longitude)
                        cleveland_oh = (content['lat'], content['lng'])
                        tempa = great_circle(newport_ri, cleveland_oh).kilometers
                        tempb = tempa / 61.25
                        distance = tempb * 100
                        if distance < 10:

                            if driver.fcmDevice:
                                try:
                                    driver.fcmDevice.send_message(
                                        data={"action": "request", "source": content['pickup'],
                                              "destination": content['destination'],
                                              'booking': booking.id})
                                except:
                                    pass
                            uid = driver.firebaseId
                            try:
                                request = {
                                    "Pickup": content['pickup'],
                                    "Destination": content['destination'],
                                    'seen': False,
                                    'BookingId': booking.id,
                                    'timestamp': booking.timestamp.strftime('%B %d, %Y %H:%M:%S')
                                }
                                requests = self.db.child("drivers").child(uid).child('requests').push(request)
                            except ValueError:
                                pass
            payload = {
                'action': 'created',
                'booking': booking.id
            }
            self.send(payload)
            self.my_stream = self.db.child("quotes").child(booking.id).stream(self.stream_handler)
        except ValueError:
            pass

    def getAllBookingInstances(self, content):
        try:
            bookings = Booking.objects.filter(client_key__iexact=content['key']).order_by('-timestamp')
            if bookings.exists():
                try:
                    payload = {
                        'action': 'bookings',
                        'bookings': json.dumps([ob.as_dict() for ob in bookings])
                    }
                    self.send(payload)
                except ValueError:
                    pass
        except ValueError:
            pass

    def expiredBookingInstances(self, content):
        try:
            if Booking.objects.filter(id=content['bookingId']).exists():
                booking = Booking.objects.get(id=content['bookingId'])
                if booking.client_key == content['key']:
                    if booking.level == 'Waiting' or booking.level == 'Confirming':
                        bid = booking.id
                        a = booking.delete()
                        payload = {
                            'action': 'delete',
                            'booking': bid
                        }
                        self.send(payload)
        except ValueError:
            pass

    def getBookingInstance(self, content):
        try:
            if Booking.objects.filter(id=content['bookingId']).exists():
                booking = Booking.objects.get(id=content['bookingId'])
                if booking.client_key == content['key']:
                    bids = Bids.objects.filter(booking=booking).values('driver').distinct()
                    drivers = Driver.objects.filter(id__in=bids)
                    bids = []
                    for driver in drivers:
                        bids.append(Bids.objects.filter(booking=booking, driver=driver).first())
                    if booking.level == 'Waiting':
                        try:
                            payload = {
                                'action': 'getBooking',
                                'booking': json.dumps(booking.as_dict()),
                                'quotes': json.dumps([ob.as_dict() for ob in bids])
                            }
                            self.send(payload)
                        except ValueError:
                            pass
                    elif booking.level == 'Confirming' or booking.level == 'Onway':
                        try:
                            myBid = None
                            for bid in bids:
                                if bid.is_final:
                                    myBid = bid
                                    break

                            payload = {
                                'action': 'getBooking',
                                'booking': json.dumps(booking.as_dict()),
                                'quotes': json.dumps([myBid.as_dict()])
                            }
                            self.send(payload)
                        except ValueError:
                            pass

        except ValueError:
            pass

    def selectBookingInstance(self, content):
        try:
            if Bids.objects.filter(id=content['bid']).exists():
                bid = Bids.objects.get(id=content['bid'])
                quote = bid.quote
                try:
                    booking = bid.booking
                    if booking.client_key != content['key']:
                        booking.client_key = content['key']
                    booking.level = 'Confirming'
                    booking.save()
                    bid.is_final = True
                    bid.save()

                    driver = bid.driver
                    if driver.fcmDevice:
                        try:
                            driver.fcmDevice.send_message(
                                data={"action": "order", 'booking': booking.id})
                        except:
                            pass

                    uid = driver.firebaseId
                    try:
                        mbids = self.db.child("drivers").child(uid).child('bids').get()
                        for bid in mbids.each():
                            temp = bid.val()
                            if temp['BookingId'] == booking.id:
                                self.db.child("drivers").child(uid).child('bids').child(bid.key()).remove()
                                break

                        request = {
                            "Pickup": booking.pickup,
                            "Destination": booking.destination,
                            'seen': False,
                            'status': booking.level,
                            'quote': quote,
                            'phone': content['phone'],
                            'BookingId': booking.id,
                            'timestamp': booking.timestamp.strftime('%B %d, %Y %H:%M:%S')
                        }
                        requests = self.db.child("drivers").child(uid).child('jobs').push(request)


                    except ValueError:
                        pass

                    payload = {
                        'action': 'confirming',
                        'booking': booking.id
                    }
                    self.send(payload)
                except ValueError:
                    pass
        except ValueError:
            pass
