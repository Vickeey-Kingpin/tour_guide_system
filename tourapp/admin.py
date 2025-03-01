from django.contrib import admin
from . models import *

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','name','email','rating','profile_photo','reviewed_date']
    ordering = ['-reviewed_date']
admin.site.register(Review,ReviewAdmin)

admin.site.register(Trip)
admin.site.register(TripBooking)
admin.site.register(Payment)
admin.site.register(Destination)
admin.site.register(Hotel)
admin.site.register(HotelBooking)

