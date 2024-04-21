from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile



# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Initialize form fields
        for field_name, field in self.fields.items():
            if self.initial.get(field_name) is None and field.required:
                self.initial[field_name] = ''

    # Validate username
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    # Validate email
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. If this is your email, please login instead.")
        return email

# User Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'default_phone_number', 'default_street_address1', 'default_street_address2',
            'default_town_or_city', 'default_postcode', 'default_country'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Initialize form fields
        for field_name in self.fields:
            if self.initial[field_name] is None:
                self.initial[field_name] = ''
