from django.urls import path
from . import views
from .views import nearest_station
app_name = 'metro'

urlpatterns = [
    path('', views.home, name='home'),
    path('fare-chart/', views.fare_chart, name='fare_chart'),  # Add this line
    path('metro_map/', views.metro_map, name='metro_map'),  # Add this line
     path('metro_stations/', views.nearest_station, name='nearest_station'),
]
