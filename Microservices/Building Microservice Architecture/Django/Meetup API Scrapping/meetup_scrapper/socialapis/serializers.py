from socialapis.models import Meetups
from rest_framework import serializers


class MeetupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meetups
        fields = ('meetup_name', 'meetup_address', 'meetup_time', 'meetup_locationx', 'meetup_locationy')



