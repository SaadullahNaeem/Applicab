from django.db import models
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice


# Models
class Driver(models.Model):
    email = models.EmailField(blank=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    firebaseId = models.CharField(max_length=300, blank=False)
    fcmDevice = models.ForeignKey(FCMDevice, blank=True, null=True)
    # location fields
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    admin_area_1 = models.CharField(max_length=100, blank=True, null=True)
    admin_area_2 = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def as_dict(self):
        return {'longitude': self.longitude, 'latitude': self.latitude, 'uid': self.firebaseId, 'taxi': self.category}


