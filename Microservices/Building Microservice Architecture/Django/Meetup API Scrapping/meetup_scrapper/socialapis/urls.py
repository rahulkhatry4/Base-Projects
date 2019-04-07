from django.conf.urls import url
from rest_framework import routers
from socialapis.views import *


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^meetups/$', MeetupsList.as_view()),
    #url(r'^meetups/(?P<pk>[0-9]+)/$', views.MeetupsDetail.as_view())
    ]