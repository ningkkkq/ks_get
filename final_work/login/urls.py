from django.urls import re_path,path
from login.views import *


urlpatterns = [
    path('', login, name='login'),
    path('signup/', signup, name='signup'),
]