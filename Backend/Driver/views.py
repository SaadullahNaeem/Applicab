from __future__ import unicode_literals

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .forms import *
from fcm_django.models import FCMDevice
from Booking.models import *
from .serializer import *

# JWT token module
from rest_framework_jwt.settings import api_settings

import pyrebase


config = {
    "apiKey": "AIzaSyA2-fkz-Acck6d8AqSkJjbBM1BQtK2NdtE",
    "authDomain": "cabs-cc162.firebaseapp.com",
    "databaseURL": "https://cabs-cc162.firebaseio.com",
    "projectId": "cabs-cc162",
    "storageBucket": "cabs-cc162.appspot.com",
    "messagingSenderId": "274763249211"
}
firebase = pyrebase.initialize_app(config)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        form = RegistrationForm(data)
        if form.is_valid():
            user = form.save(data)
            if user is not None:
                auth = firebase.auth()
                temp = auth.create_user_with_email_and_password(data['email'], data['password1'])
                firebase_id = temp['localId']
                payload = jwt_payload_handler(user)
                access_token = jwt_encode_handler(payload)

                return Response(
                    {'result': 'success', 'access_token': access_token, 'email': user.email, 'uid': firebase_id},
                    status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_200_OK)


class DriverRegisterView(APIView):
    def post(self, request):
        get_data = request.data
        form = DriverRegistrationForm(request.data)

        user_name = get_data['email'].rsplit('@', 1)[0]
        username = ''
        for i in range(100):
            if i:
                username = "%s%s" % (user_name, i)
            else:
                username = "%s" % user_name
            if not User.objects.filter(username__iexact="%s" % user_name).exists():
                break

        if form.is_valid():
            if User.objects.filter(Q(email__exact=get_data['email']) | Q(
                    username__exact=username)).exists():
                return Response({'errors': {'__all__': ['User already Exists against this Email']}},
                                status=status.HTTP_200_OK)
            else:
                instance = form.save(commit=False)

                password = get_data['password']
                user = User.objects.create(first_name=get_data['first_name'], username=username,
                                           last_name=get_data['last_name'], email=get_data['email'],
                                           password=make_password(password))
                user.save()
                instance.user = user

                auth = firebase.auth()

                temp = auth.create_user_with_email_and_password(get_data['email'], password)

                instance.firebaseId = temp['localId']
                instance.save()

                # Get a reference to the database service
                db = firebase.database()

                # data to save
                data = {
                    "FirstName": user.first_name,
                    "LastName": user.last_name,
                    "PhoneNumber": instance.phone_number
                }

                results = db.child("drivers").child(temp['localId']).set(data)

                if user is not None:
                    payload = jwt_payload_handler(user)
                    access_token = jwt_encode_handler(payload)

                return Response(
                    {'result': 'success', 'access_token': access_token,
                     'email': user.email, 'uid': instance.firebaseId},
                    status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_200_OK)


class SigninView(APIView):
    def post(self, request):
        data = request.data
        if not 'email' in data or not 'password' in data:
            return Response({'errors': {'__all__': ['Email and Password is required']}},
                            status=status.HTTP_200_OK)

        check_user = User.objects.filter(email__iexact=data['email'])
        if check_user.exists():
            user = check_user.first()
            password = data['password']

            if user is not None and user.check_password(password):
                payload = jwt_payload_handler(user)
                access_token = jwt_encode_handler(payload)

                return Response(
                    {'result': 'success', 'access_token': access_token, 'email': user.email, 'uid': user.id},
                    status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'__all__': ['Email and Password are not matched']}},
                                status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'__all__': ['No Driver is registered against this Email']}},
                            status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request):
        request.session.clear()
        logout(request)
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


class IsBIActiveView(APIView):
    def get(self, request,id):
        if Booking.objects.filter(id=id).exists():
            book = Booking.objects.get(id=id)
            if book.level == 'Waiting':
                return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_200_OK)


class IsBIConfirmView(APIView):
    def get(self, request,id):
        if Booking.objects.filter(id=id).exists():
            book = Booking.objects.get(id=id)
            if book.level == 'Confirming':
                return Response({'result': True,'confirm': False}, status=status.HTTP_200_OK)
            elif book.level == 'Onway':
                return Response({'result': True, 'confirm': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_200_OK)


class AcceptView(APIView):
    def get(self, request,id):
        if Booking.objects.filter(id=id).exists():
            book = Booking.objects.get(id=id)
            if book.level == 'Confirming':
                book.level = 'Onway'
                book.save()
                return Response({'result': True}, status=status.HTTP_200_OK)
            else:
                return Response({'result': False}, status=status.HTTP_200_OK)

        return Response({'result': False}, status=status.HTTP_200_OK)


class DriverFcmView(APIView):
    def post(self, request):
        data = request.data
        uid = data['uid']
        fcm = data['fcm']

        check_driver = Driver.objects.filter(firebaseId__iexact=data['uid'])
        if check_driver.exists():
            driver = Driver.objects.get(firebaseId__iexact=data['uid'])
            check_fcm = FCMDevice.objects.filter(registration_id__iexact=data['fcm'])
            if check_fcm.exists():
                fcm = FCMDevice.objects.get(registration_id__iexact=data['fcm'])
                driver.fcmDevice = fcm
                driver.save()
                return Response(
                    {'result': 'success', 'did': driver.id}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'__all__': ['No Driver or FCM is registered against this firebase Id']}},
                                status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'__all__': ['No Driver is registered against this firebase Id']}},
                            status=status.HTTP_200_OK)


class Profile(APIView):
    db = firebase.database()

    def post(self, request):
        data = request.data
        driver = Driver.objects.filter(firebaseId__iexact=data['firebaseId'])
        if driver.exists():
            driver = Driver.objects.get(firebaseId__iexact=data['firebaseId'])
            form = DriverProfileForm(request.data, instance=driver)
            if form.is_valid():
                form.save()
                payload = {
                    "name": data['name'],
                    "phone_number": data['phone_number'],
                    "language": data['language'],
                    "category": data['category'],
                    "email": data['email'],
                }
                try:
                    self.db.child("drivers").child(data['firebaseId']).child('profile').set(payload)
                except:
                    pass
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': form.errors}, status=status.HTTP_200_OK)

        else:
            form = DriverProfileForm(request.data)
            if form.is_valid():
                form.save()
                payload = {
                    "name": data['name'],
                    "phone_number": data['phone_number'],
                    "language": data['language'],
                    "category": data['category'],
                    "email": data['email'],
                }
                try:
                    self.db.child("drivers").child(data['firebaseId']).child('profile').set(payload)
                except:
                    pass
                return Response({'result': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': form.errors}, status=status.HTTP_200_OK)
