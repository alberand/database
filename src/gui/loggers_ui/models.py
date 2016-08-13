from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Loggers(models.Model):
    ses_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'loggers'

    def __str__(self):
        return str(self.ses_id)


class Messages(models.Model):
    ses_id = models.IntegerField()
    msg = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'messages'

    def __str__(self):
        return 'Session: {}. Type: T. Message: {}'.format(self.ses_id, self.msg)


class Packages(models.Model):
    module_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    t_ms = models.IntegerField()
    latitude = models.FloatField()
    lat_pos = models.CharField(max_length=1)
    longitude = models.FloatField()
    lon_pos = models.CharField(max_length=1)
    course = models.FloatField()
    gps_altitude = models.FloatField()
    speed = models.FloatField()
    temperature = models.IntegerField()
    pressure = models.IntegerField()
    gps_state = models.IntegerField()
    sat_num = models.IntegerField()
    ses_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'packages'

    def __str__(self):
        return 'Session: {}. Type: D. Time: {}'.format(self.ses_id, self.time)
