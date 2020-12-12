from django.urls import path
from play_video.views import *

urlpatterns = [
    path('', index, name='getStart'),
    path('logout/', logout)
]
