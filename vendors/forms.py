from django import forms
from vendors.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
            model = User
            fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    MY_CHOICES = (
        ('1', 'Vendor'),
        ('2', 'Farmer'),
    )
    position = forms.ChoiceField(choices=MY_CHOICES)
    class Meta:
        model = UserProfile
        fields = ('location', 'position')

class GoogleMapForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('map_lon', 'map_lat')