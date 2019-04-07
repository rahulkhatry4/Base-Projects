from django.conf.urls import url
from rest_framework import routers
from sensordata.views import *

urlpatterns = [
    url(r'^sensordata/$', SensorDataList.as_view()),
    ]