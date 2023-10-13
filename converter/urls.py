from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('downloadmp4', views.downloadmp4, name="Downloadmp4"),
    
]