from django.contrib import admin

from booking.models import Booking, AcademyClass

# Register your models here.
admin.site.register(Booking)
admin.site.register(AcademyClass)
