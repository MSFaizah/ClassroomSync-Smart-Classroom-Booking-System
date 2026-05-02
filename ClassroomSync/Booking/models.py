from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
'''
Django is very picky about table names. By default, Django looks for a table called booking_rooms (app name + underscore + model name).

If you manually created a table in MySQL Workbench named simply rooms or Rooms, Django will not find your data. It will look at the empty table it created for itself (booking_rooms) and return [].

You can tell Django exactly which table to look at by adding a Meta class to your model
'''

class Rooms(models.Model):
    room_number = models.CharField(max_length=50, primary_key=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default="Available")

    class Meta:
        db_table = 'rooms'

class RequestApplications(models.Model):
    aim = models.CharField(max_length=20)
    room = models.CharField(max_length=50)
    requester = models.CharField(max_length=100)
    uid = models.CharField(max_length=8)
    dept = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    
class AdminLogins(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    class Meta:
        db_table = 'adminlogins'
    
class Bookings(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    room_number = models.ForeignKey(Rooms, db_column= 'room_number', on_delete=models.CASCADE, null=False, blank=False)

    # on_delete = models.SET_NULL -> If the related object is deleted, this field will become NULL
    # on_delete = models.CASCADE -> If the related object is deleted, this field will be deleted

    requested_by = models.CharField(max_length=100)
    department =  models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, default='Available')
    class Meta:
        db_table = 'bookings'
    
class Alert(models.Model):
    TYPE_CHOICES = [('blocked', 'Blocked'),('notice', 'Notice'),('info', 'Info')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    alert_date = models.DateField(default = datetime.date.today)
    alert_start_time = models.TimeField(default = datetime.time(12, 0))
    alert_end_time = models.TimeField(default = datetime.time(12, 0))
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)