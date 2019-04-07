from django.db import models


class Meetups(models.Model):
    meetup_name = models.CharField(max_length=200)
    meetup_address = models.CharField(max_length = 1000)
    meetup_time = models.DateTimeField(auto_now = False)
    meetup_locationx = models.FloatField()
    meetup_locationy = models.FloatField()

    def __str__(self):
        return str(self.meetup_name) + ' ' + str(self.meetup_address)