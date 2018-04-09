from django.urls import path
from rest_framework import routers

from .views import *
app_name = 'user-api'
router = routers.SimpleRouter()
router.register(r'posts', PostView, base_name='posts')
router.register(r'users', UserView, base_name='users')
router.register(r'likes', LikeView, base_name='likes')


