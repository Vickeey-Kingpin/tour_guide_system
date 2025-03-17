from django.contrib import admin
from . models import *

# Register your models here.
def confirm_payment(modeladmin,request,queryset):
    queryset.update(paid=True)
confirm_payment.short_description = 'Confirm payment'   

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','name','email','rating','profile_photo','reviewed_date']
    ordering = ['-reviewed_date']

class TripBookingAdmin(admin.ModelAdmin):
    list_display = ['user','trip','email','adult','children','date']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','booked_for','payment_option','amount_paid','paid','payment_number']
    actions =[confirm_payment]

admin.site.register(Review,ReviewAdmin)

admin.site.register(Trip)
admin.site.register(TripBooking,TripBookingAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Destination)
admin.site.register(Hotel)
admin.site.register(HotelBooking)
admin.site.register(Staff)

