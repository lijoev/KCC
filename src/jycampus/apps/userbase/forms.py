import logging
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from .models import Profile, Participants
from datetime import datetime
LOG = logging.getLogger('myStock.%s' % __name__)


class LoginForm(forms.Form):
    """
    Login form which deals with login process of a user.
    All fields are must field.
    """
    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': "form-control", 'id': 'email'}),
        help_text=_('Users can login using their username')
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))


class DateInput(forms.DateInput):
    input_type = 'date'


class AddParticipantsForm(forms.ModelForm):
    """
    sign up form which deals with signup process.
    all fields are must fields
    """
    YEARS = [x for x in range(1940, 2021)]
    STREAM_CHOICES = (('None', 'Select Stream'), ('TASC', 'Arts and Science'), ('Engineering', 'Engineering'),('Medical', 'Medical'),
               ('Nursing', 'Nursing'), ('Polytechnic', 'Polytechnic'),
               ('ITI', 'ITI'), ('Law', 'Law'), ('Hotel Management', 'Hotel Management'), ('Others', 'Others'))
    SUBREGION_CHOICES = (('None', 'Select Subregion'), ('North', 'North'), ('Malabar', 'Malabar'), ('North central', 'North central'),
                      ('Central', 'Central'), ('Eastern', 'Eastern'),
                      ('South central', 'South central'), ('South', 'South'),)
    ZONE_CHOICES = (('None', 'Select Zone'), ('Kasargod', 'Kasargod'), ('Thalassery', 'Thalassery'), ('Manathaady', 'Manathaady'),
                         ('Calicut', 'Calicut'), ('Palakkad', 'Palakkad'),
                         ('Thrissur', 'Thrissur'), ('Irinjalakkuda', 'Irinjalakkuda'),
                    ('Angamaly', 'Angamaly'), ('Ernakulam', 'Ernakulam'),
                    ('Cherthala', 'Cherthala'), ('Alleppey', 'Alleppey'),
                    ('Kothamangalam', 'Kothamangalam'), ('Idukki', 'Idukki'),
                    ('Kattapana', 'Kattapana'), ('Pala', 'Pala'),
                    ('Kanjirapally', 'Kanjirapally'),
                    ('Kottayam', 'Kottayam'),
                    ('Chenganasserry', 'Chenganasserry'), ('Punalur', 'Punalur'),
                    ('Kollam', 'Kollam'), ('Trivandrum', 'Trivandrum'), ('Neyyatinkara', 'Neyyatinkara'),)

    name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': "form-control"}))

    dob = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD"}))
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    phoneNumber = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control"}))
    college = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': "form-control"}))
    stream = forms.CharField(widget=forms.Select(choices=STREAM_CHOICES, attrs={'class': "form-control"}))
    subregion = forms.CharField(widget=forms.Select(choices=SUBREGION_CHOICES, attrs={'class': "form-control"}))
    zone = forms.CharField(widget=forms.Select(choices=ZONE_CHOICES, attrs={'class': "form-control"}))

    class Meta:
        model = Participants
        fields = ('name', 'dob', 'email', 'phoneNumber', 'college', 'stream', 'subregion', 'zone')



class ProfileForm(forms.ModelForm):
    """
    Form to update user profile
    """
    about_me = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': "form-control"}))
    profile_pic = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': "form-control"}))

    class Meta:
        model = Profile
        fields = ('profile_pic', 'about_me')


class UpdateUserForm(forms.ModelForm):
    """
    form which handles user details updation
    """
    nick_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    is_subscribed = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('nick_name', 'full_name', 'is_subscribed')