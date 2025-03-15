from django.urls import path
from . import views
from .views import nearest_station,terms_of_service, privacy_policy
app_name = 'metro'

urlpatterns = [
    path('', views.home, name='home'),
    path('fare-chart/', views.fare_chart, name='fare_chart'),
    path('metro_map/', views.metro_map, name='metro_map'),  
     path('metro_stations/', views.nearest_station, name='nearest_station'),
         path('terms_of_service/', terms_of_service, name='terms_of_service'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]
