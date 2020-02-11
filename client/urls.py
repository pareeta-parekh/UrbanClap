from django.contrib import admin
from django.urls import path , include
from .users import *
from .services import *
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/' , login),
    path('showService/' , showServices),
    path('category/' , categoryShow ),
]