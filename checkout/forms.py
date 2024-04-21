from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        # Define the model and fields for the form
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form:
        - Add placeholders and classes
        - Remove auto-generated labels
        - Set autofocus on the first field
        """
        super().__init__(*args, **kwargs)

        # Define placeholders for each field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
        }

        # Set autofocus on the 'full_name' field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Iterate over each field in the form
        for field in self.fields:
            # If the field has no initial value, set it to an empty string
            if not self.initial.get(field):
                self.fields[field].initial = ""

            # If the field is required, add an asterisk to the placeholder
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            # Set the placeholder and class for the field's widget
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

            # Remove the field's label
            self.fields[field].label = False