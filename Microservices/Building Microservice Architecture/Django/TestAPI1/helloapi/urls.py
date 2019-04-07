from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls import url
from .views import *


router = routers.DefaultRouter()
router.register(r'hello', MessageViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
    ]