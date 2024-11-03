# metro_navigation/metro/models.py
from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    line_color = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    is_interchange = models.BooleanField(default=False)  # New field for interchanges

    def __str__(self):
        return f"{self.name} ({self.line_color})"

class Connection(models.Model):
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='outgoing_connections')
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='incoming_connections')
    distance = models.IntegerField(help_text="Distance in meters")
    time = models.IntegerField(help_text="Time in minutes")

    class Meta:
        unique_together = ['from_station', 'to_station']

    def __str__(self):
        return f"{self.from_station.name} → {self.to_station.name}"