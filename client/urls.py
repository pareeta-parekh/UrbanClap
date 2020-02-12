from django.contrib import admin
from django.urls import path , include
from .users import *
from .services import *
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/' , login),
    path('logout/<str:token>/', logout),
    path('showService/' , showServices),
    path('category/<str:token>/' , categoryShow ),
    path('req_service/<str:token>/' , req_service),
    path('del_Service/' , deleteService),
]