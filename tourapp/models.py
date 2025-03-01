from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

# Create your models here.
PAYMENT_OPTIONS = (
    ('Mpesa','M'),
    ('Paypal','P')
)
SITES_OPTIONS = (
    ('Game Park','GP'),
    ('Museum','M'),
    ('Airport','A')
)

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.CharField(max_length=500)
    rating = models.IntegerField()
    profile_photo = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    reviewed_date = models.DateTimeField(auto_now=True)    

class Trip(models.Model):
    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=500)
    inclusive = models.CharField(max_length=500)
    exclusive = models.CharField(max_length=500)
    image1 = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    image2 = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    image3 = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    image4 = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    accomodation = models.FloatField(default=0)	
    transport = models.FloatField(default=0)	 
    meals = models.FloatField(default=0)		
    others = models.FloatField(default=0)	

    def get_absolute_url(self):
        return reverse('trip', kwargs={'pk':self.pk})
    
    def get_trip_total_amount(self):
        return round(self.accomodation + self.transport + self.meals + self.others)

    def get_paypal_trip_total_amount(self):
        paypal_trip_total = self.accomodation + self.transport + self.meals + self.others
        return round(paypal_trip_total/135)
 
class TripBooking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    adult = models.IntegerField()
    children= models.IntegerField()
    date = models.DateField(default=timezone.now)
    # booked = models.BooleanField(default=False)

    # def get_booking_adult_totals(self):
    #     return round(int(self.trip.get_trip_total_amount())*int(self.adult))
    
    def get_children_totals(self):
        return round(0.5 * int(self.trip.get_trip_total_amount()))
    
    def get_all_total(self):
        adult_total = self.adult * self.trip.get_trip_total_amount()
        children_total = self.children * self.get_children_totals()
        return adult_total + children_total
    
    def get_paypal_children_totals(self):
        total = int(self.get_children_totals())/135
        return round(total)
    
    def get_paypal_all_total(self):
        total = int(self.get_all_total())/135
        return round(total)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_option = models.CharField(max_length=10,choices=PAYMENT_OPTIONS)

class Destination(models.Model):
    title = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='images/',default='images/giraffe.jpg')
    site = models.CharField(max_length=15,choices=SITES_OPTIONS)

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    hotel_photo = models.ImageField(upload_to='images/',default='images/villarosa.jpg')
    price = models.FloatField()
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse('hoteldetails', kwargs={'pk':self.pk})

    def get_price(self):
        return round(self.price)
    
    def get_children_total(self):
        children_total = round(0.5 * self.price) 
        return children_total
    
    def get_paypal_price(self):
        total = int(self.get_price())/135
        return round(total)
    
    def get_paypal_children_total(self):
        total = int(self.get_children_total())/135
        return round(total)
    
class HotelBooking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,null=True,blank=True)
    full_name=models.CharField(max_length=100)
    email = models.EmailField()
    period = models.IntegerField()
    adult = models.IntegerField()
    children = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def get_adult_totals(self):
        adult_total = int(self.hotel.get_price()) * int(self.period) * int(self.adult)
        return adult_total

    def get_children_totals(self):
        children_total = 0.5*(int(self.hotel.get_price()) * int(self.period) * int(self.children))
        return round(children_total)
    
    def get_total_price(self):        
        total = int(self.get_adult_totals()) + int(self.get_children_totals())
        return total
    
    def get_paypal_total_price(self):
        total = int(self.get_total_price())/135
        return round(total)
