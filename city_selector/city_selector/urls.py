from django.contrib import admin
from django.urls import path
from .views import select_city

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', select_city, name="select_city"),
]
