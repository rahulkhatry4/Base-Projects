from sensordata.models import SensorData
from rest_framework import serializers


class SensorDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorData
        fields = ('userid', 'locationx', 'locationy', 'accelerationx', 'accelerationy', 'datatime')