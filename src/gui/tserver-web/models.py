from __future__ import unicode_literals

from django.db import models
from django.template.defaulttags import register

@register.filter
def get_package_fields(package, field):
    return package.get(field)

class Sessions(models.Model):
    ses_id = models.CharField(primary_key=True, max_length=11)

    class Meta:
        managed = False
        db_table = 'sessions'

    def getDate(self):
        return Packages.objects.filter(ses_id=self.ses_id).earliest('date').date

class Messages(models.Model):
    ses = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    ses_time = models.TimeField(blank=True, null=True)
    msg = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'messages'


class Packages(models.Model):
    ses = models.ForeignKey(Sessions, on_delete=models.CASCADE)
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
    gsm_sig_str = models.FloatField(blank=True, null=True)
    net_provider = models.CharField(max_length=20, blank=True, null=True)
    network_type = models.CharField(max_length=5, blank=True, null=True)
    x_acc = models.FloatField(blank=True, null=True)
    y_acc = models.FloatField(blank=True, null=True)
    z_acc = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'packages'


