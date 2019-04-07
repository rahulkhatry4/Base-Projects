from rest_framework import serializers
from helloapi.models import Message

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('message', 'message_date_time')