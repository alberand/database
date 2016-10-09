from __future__ import unicode_literals

from django.db import models


class Sessions(models.Model):
    ses_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sessions'

class Packages(models.Model):
    ses = models.ForeignKey('Sessions', models.DO_NOTHING)
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

    class Meta:
        managed = False
        db_table = 'packages'

class Messages(models.Model):
    ses = models.ForeignKey('Sessions', models.DO_NOTHING)
    msg = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'messages'

