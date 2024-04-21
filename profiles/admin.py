from django.contrib import admin
from .models import Profile


# Local Profile model import

# Define a custom admin interface for the Profile model
class ProfileAdmin(admin.ModelAdmin):
    # Fields to be displayed in list views
    list_display = (
        'user', 
        'default_phone_number', 
        'default_street_address1', 
        'default_street_address2', 
        'default_town_or_city', 
        'default_postcode', 
        'default_country'
    )

    # Fields to be searched in the admin site
    search_fields = ('user__username',)

# Register the custom admin interface for the Profile model
admin.site.register(Profile, ProfileAdmin)
