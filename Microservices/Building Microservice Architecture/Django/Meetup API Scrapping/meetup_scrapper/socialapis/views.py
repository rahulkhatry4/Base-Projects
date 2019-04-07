from socialapis.models import Meetups
from sensordata.models import SensorData
from socialapis.serializers import MeetupsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import requests

def processing_function(request, meetups):
	sensordata_objects = SensorData.objects.filter(userid = request.user)
	all_sensor_readings = list(sensordata_objects)
	number_of_readings = len(all_sensor_readings)
	user_xlocation = all_sensor_readings[number_of_readings - 1].locationx
	user_ylocation = all_sensor_readings[number_of_readings - 1].locationy

	request1 = requests.get('https://api.meetup.com/2/cities')
	
	needed_location_x = user_xlocation
	needed_location_y = user_ylocation
	x_window = 0.5
	y_window = 0.5

	request1 = requests.get('https://api.meetup.com/find/upcoming_events?key=29737346994f1d2c6e15c633a1d79')
	output_json = request1.json()
	#output_json['events'][0]['group']['name']
	for element in output_json['events']:
		meetup_name_val = element['name']
		meetup_location_local_date_val = element['local_date']
		meetup_location_local_time_val = element['local_time']
		meetup_datetime_val = meetup_location_local_date_val + ' ' + meetup_location_local_time_val
		meetup_datetime_object = datetime.strptime(meetup_datetime_val, '%Y-%m-%d %H:%M')

		try:
			metup_address_val = element['venue']['address_1']
			meetup_city_val = element['venue']['city']
			meetup_location_lat_val = element['venue']['lat']
			meetup_location_lon_val = element['venue']['lon']
		except:
			metup_address_val = element['group']['name']
			meetup_city_val = element['group']['localized_location']
			meetup_location_lat_val = element['group']['lat']
			meetup_location_lon_val = element['group']['lon']

		Meetups.objects.get_or_create(
			meetup_name=meetup_name_val,
			meetup_address=metup_address_val,
			meetup_time = meetup_datetime_object,
			meetup_locationx = meetup_location_lat_val,
			meetup_locationy = meetup_location_lon_val
			)

    #name, venue address, city, latitude, longitude

	relevant_meetups = Meetups.objects.filter(meetup_locationx__gte = (needed_location_x - x_window)).filter(meetup_locationx__lte = (needed_location_x + x_window)).filter(meetup_locationy__gte = (needed_location_y - y_window)).filter(meetup_locationy__lte = (needed_location_y + y_window))
	all_meetups = list(relevant_meetups)
	print(all_meetups)

	return relevant_meetups


class MeetupsList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        meetups = Meetups.objects.all()
        relevant_meetups = processing_function(request, meetups)
        serializer = MeetupsSerializer(relevant_meetups, many=True)
        return Response(serializer.data)



# class MeetupsDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Meetups.objects.get(pk=pk)
#         except Meetups.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         meetups = self.get_object(pk)
#         serializer = MeetupsSerializer(snippet)
#         return Response(serializer.data)