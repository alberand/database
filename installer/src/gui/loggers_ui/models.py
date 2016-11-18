from __future__ import unicode_literals

from django.db import models


class Sessions(models.Model):
    ses_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sessions'

class Packages(models.Model):
    ses = models.ForeignKey('Sessions', models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    t_ms = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    lat_pos = models.CharField(max_length=1, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    lon_pos = models.CharField(max_length=1, blank=True, null=True)
    course = models.FloatField(blank=True, null=True)
    gps_altitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    gps_state = models.IntegerField(blank=True, null=True)
    sat_num = models.IntegerField(blank=True, null=True)
    gps_sig_str = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'packages'

class Messages(models.Model):
    ses = models.ForeignKey('Sessions', models.DO_NOTHING)
    msg = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'messages'

