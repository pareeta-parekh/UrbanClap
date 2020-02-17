from django.contrib import admin
from django.urls import path , include
from .users import *
from .services import *
from .views import *
from .chat import *

urlpatterns = [
    path('register/', register),
    path('login/' , login),
    path('logout/', logout),
    path('show_service/' , showServices),
    path('category/' , categoryShow ),
    path('chat/<int:srpr_id>/<int:service_id>/', client_chat),
    path('req_service/' , req_service),
    path('del_service/' , deleteService),
    path('update_password/', updatepass),
    path('comments/' ,comments),
]