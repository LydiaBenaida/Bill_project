from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.models import User, Group

from bill.models import Client


class RegistrationForm(UserCreationForm):
    email=forms.EmailField()

    adresse =forms.CharField(max_length=200)
    tel = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ["username","email","password1","password2","last_name","first_name","adresse","tel"]
