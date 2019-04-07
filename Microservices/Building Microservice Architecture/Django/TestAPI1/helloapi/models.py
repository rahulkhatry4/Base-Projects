from django.db import models

# Create your models here.

class Message(models.Model):
    message = models.TextField(max_length=200)
    message_date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message + ' ' + str(self.message_date_time)