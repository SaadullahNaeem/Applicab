from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^register', RegisterView.as_view()),
    url(r'^signin', SigninView.as_view()),
    url(r'^driver/fcm', DriverFcmView.as_view()),
    url(r'^driver/profile', Profile.as_view()),
    url(r'^logout', LogoutView.as_view()),
    url(r'^booking/(?P<id>[0-9]+)/', IsBIActiveView.as_view()),
    url(r'^booking/confirm/(?P<id>[0-9]+)/', IsBIConfirmView.as_view()),
    url(r'^booking/accept/(?P<id>[0-9]+)/', AcceptView.as_view()),
]