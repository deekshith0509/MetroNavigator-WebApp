from django.contrib import admin
from .models import Station, Connection

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'line_color')
    search_fields = ('name', 'code')
    list_filter = ('line_color',)

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_station', 'to_station', 'distance', 'time')
    search_fields = ('from_station__name', 'to_station__name')
    list_filter = ('from_station__line_color', 'to_station__line_color')
