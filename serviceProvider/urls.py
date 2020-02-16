from django.urls import path, include
from .users import *
from .services import *
from .chat import *

urlpatterns = [
    path('register/', spregister),
    path('login/', sprlogin),
    path('logout/', sprlogout),
    path('addservice/', addservice),
    path('appliedservices/',appliedservices),
    path('updateservice/', updateservice),
    path('deletereq/', deleteservice),
    path('chat/<int:cust_id>/<int:service_id>/', srpr_chat),
    path('updatepassword/', updatepass),
]