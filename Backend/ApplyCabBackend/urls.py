"""ApplyCabBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from ApplyCabBackend import settings

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^zkjih3y3bi3u9dbjnnn9no8hyughvbv2j8jh7d7/api/', include('Driver.urls')),
    url(r'^', include(router.urls))
]
# urlpatterns += [
#     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.STATIC_ROOT,
#     }),
# ]