from django.contrib import admin
from .models import Order, OrderLineItem


# Define the inline admin interface for OrderLineItem
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

# Define the admin interface for Order
class OrderAdmin(admin.ModelAdmin):
    # Inline editing of OrderLineItem objects in the Order admin
    inlines = (OrderLineItemAdminInline,)

    # Fields to display as read-only
    readonly_fields = ('order_number', 'date', 'order_total', 'grand_total',)

    # Fields to display in the Order form
    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1', 'street_address2',
              'order_total', 'grand_total',)

    # Fields to display in the Order list
    list_display = ('order_number', 'date', 'full_name', 'order_total', 'grand_total',)

    # Default sorting is by date in descending order
    ordering = ('-date',)

# Register the admin class with the associated model
admin.site.register(Order, OrderAdmin)
