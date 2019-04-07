from django.db import models

class SensorData(models.Model):
    userid = models.CharField(max_length=200)
    locationx = models.FloatField()
    locationy = models.FloatField()
    accelerationx = models.FloatField()
    accelerationy = models.FloatField()
    datatime = models.DateTimeField(auto_now = True)


    def __str__(self):
        return str(self.userid) + ' ' + str(self.locationx)