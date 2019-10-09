from django import forms
from .models import Driver
from django.contrib.auth.models import User


class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('phone_number', 'language',)


class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'email', 'category', 'phone_number', 'language', 'firebaseId')


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.TextInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if Driver.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("The email is already registered. Please use another one.")
        return email

    def save(self, data, *arg, **kw):
        username = self.create_username(data['email'])
        user = User(username=username,
                    email=data['email'])
        user.set_password(data['password1'])
        user.save()
        return user

    def create_username(self, email):
        user_name = email.rsplit('@', 1)[0]
        username = ''
        for i in range(100):
            if i:
                username = "%s%s" % (user_name, i)
            else:
                username = "%s" % user_name
            if not User.objects.filter(username__iexact="%s" % user_name).exists():
                break
        return username

    class Meta:
        model = User
        fields = ('email',)
