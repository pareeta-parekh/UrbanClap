from django.urls import path, include
from .users import *
from .services import *
from .chat import *

urlpatterns = [
    path('register/', spregister),
    path('login/', sprlogin),
    path('logout/<str:token>/', sprlogout),
    path('addservice/<str:token>/', addservice),
    path('updateservice/<str:asid>/<str:token>/', updateservice),
    path('deletereq/<str:sid>/<str:token>/', deleteservice),
    path('chat/<str:token>/<int:cust_id>/<int:service_id>/', srpr_chat),
]