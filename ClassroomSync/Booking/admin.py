from django.contrib import admin
from .models import Rooms, AdminLogins, Bookings
# Register your models here.
admin.site.register(Rooms)
admin.site.register(AdminLogins)
admin.site.register(Bookings)