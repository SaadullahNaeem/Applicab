from __future__ import unicode_literals

from django.db import models

from Driver.models import Driver


class Booking(models.Model):
    client_key = models.CharField(max_length=100, blank=True)
    pickup = models.CharField(max_length=150, blank=False)
    destination = models.CharField(max_length=150, blank=False)
    level = models.CharField(max_length=150, blank=True)
    timestamp = models.DateTimeField(auto_now=True, editable=False)

    def as_dict(self):
        return {'pickup': self.pickup, 'timestamp': self.timestamp.strftime('%B %d, %Y %H:%M:%S'), 'destination': self.destination, 'level': self.level, 'id': self.id}


class Bids(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=False)
    quote = models.CharField(max_length=100, blank=True,null=True)
    is_final = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True, editable=False)

    def as_dict(self):
        return {'booking': self.id, 'quote': self.quote, 'timestamp': self.timestamp.strftime('%B %d, %Y %H:%M:%S'), 'location': self.driver.as_dict()}