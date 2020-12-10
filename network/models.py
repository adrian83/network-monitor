from django.db import models

class Metrics(models.Model):
    download_speed = models.FloatField()
    download_error = models.CharField(max_length=200, null=True, blank=True)
    upload_speed = models.FloatField()
    upload_error = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField('date')

    def __str__(self):
        return "Metrics [download speed: {0}, download error: {1}, upload speed: {2}, upload error: {3}, date: {4}]".format(self.download_speed, self.download_error, self.upload_speed, self.upload_error, self.date)
