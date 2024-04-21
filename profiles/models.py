from django.db import models
from django.contrib.auth.models import User

# Django imports

# Profile model
class Profile(models.Model):
    # Link to User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Contact details
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = models.CharField(max_length=40, null=True, blank=True)

    # String representation of the model
    def __str__(self):
        return self.user.username
