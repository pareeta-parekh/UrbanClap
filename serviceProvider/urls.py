from django.urls import path, include
from .users import *
from .services import *

urlpatterns = [
    path('spregister/', spregister),
    path('login/', sprlogin),
    path('logout/<str:token>/', sprlogout),
    path('addservice/<str:token>/', addservice),
    path('updateservice/<str:asid>/<str:token>/', updateservice),
    path('deletereq/<str:sid>/<str:token>/', deleteservice)
]