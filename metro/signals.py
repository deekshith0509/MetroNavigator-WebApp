from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Connection

@receiver(post_save, sender=Connection)
def create_reverse_connection(sender, instance, created, **kwargs):
    """
    Automatically create reverse connection when a new connection is created
    """
    if created:
        Connection.objects.get_or_create(
            from_station=instance.to_station,
            to_station=instance.from_station,
            defaults={
                'distance': instance.distance,
                'time': instance.time
            }
        )