from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem


# This receiver is triggered after a save event on the OrderLineItem model
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    # Update the total on the related Order instance
    instance.order.update_total()

# This receiver is triggered after a delete event on the OrderLineItem model
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    # Update the total on the related Order instance
    instance.order.update_total()