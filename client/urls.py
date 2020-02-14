from django.contrib import admin
from django.urls import path , include
from .users import *
from .services import *
from .views import *
from .chat import *

urlpatterns = [
    path('register/', register),
    path('login/' , login),
    path('logout/<str:token>/', logout),
    path('showService/' , showServices),
    path('category/' , categoryShow ),
    path('chat/<str:token>/<int:srpr_id>/<int:service_id>/', client_chat),
    path('req_service/' , req_service),
    path('del_Service/' , deleteService),
    path('updatepassword/<str:token>/', updatepass),
    path('comments/' ,comments),
]