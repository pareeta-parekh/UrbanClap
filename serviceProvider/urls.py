from django.urls import path, include
from .users import *
from .services import *

urlpatterns = [
    path('spregister/', spregister),
    path('addservice/<str:pk>/', addservice),
    path('updateservice/<str:asid>/<str:spid>/', updateservice),
    path('deletereq/<str:sid>/<str:spid>/', deleteservice)
]