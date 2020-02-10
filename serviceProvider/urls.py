from django.urls import path, include
from .users import *
from .services import *

urlpatterns = [
    path('spregister/', spregister),
    path('addservice/', addservice)
]