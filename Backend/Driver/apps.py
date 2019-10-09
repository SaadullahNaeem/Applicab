from django.apps import AppConfig
import pyrebase


# config = {
#     "apiKey": "AIzaSyA2-fkz-Acck6d8AqSkJjbBM1BQtK2NdtE",
#     "authDomain": "cabs-cc162.firebaseapp.com",
#     "databaseURL": "https://cabs-cc162.firebaseio.com",
#     "projectId": "cabs-cc162",
#     "storageBucket": "cabs-cc162.appspot.com",
#     "messagingSenderId": "274763249211"
# }
# firebase = pyrebase.initialize_app(config)

class DriverConfig(AppConfig):
    name = 'Driver'

    # def location_handler(self, message):
    #     Driver = self.get_model('Driver')
    #     paths = []
    #     paths = message['path'].strip('/').split('/')
    #
    #     if len(paths) == 2:
    #         if paths[1] == 'location':
    #             if Driver.objects.filter(firebaseId__iexact=paths[0]).exists():
    #                 driver = Driver.objects.get(firebaseId__iexact=paths[0])
    #                 data = message["data"]
    #                 driver.country = data['country']
    #                 driver.admin_area_1 = data['area_level1']
    #                 driver.admin_area_2 = data['area_level2']
    #                 driver.latitude = data['lat']
    #                 driver.longitude = data['lng']
    #                 driver.save()
    #
    # def ready(self):
    #     db = firebase.database()
    #     location_stream = db.child("drivers").stream(self.location_handler)