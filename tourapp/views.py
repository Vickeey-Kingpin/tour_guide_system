from django.shortcuts import render,redirect,get_list_or_404,reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import *
from django.views.generic import View,ListView,DetailView
from . forms import *
from django.core.exceptions import ObjectDoesNotExist
import folium
from folium.features import CustomIcon
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
def form_validity(values):
    valid = True
    for fields in values:
        if fields == "":
            valid=False
    return valid

class HomeView(ListView):
    def get(self,*args,**kwargs):
        reviews = Review.objects.all().order_by('-reviewed_date')[:4]
        trips = Trip.objects.all()
        destinations = Destination.objects.all()
        destinations_count = destinations.count()
        context={
        'reviews':reviews,
        'trips':trips,
        'destinations':destinations,
        'destinations_count':destinations_count
        }
        return render(self.request, 'home.html',context)

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if len(password)>=8:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'This email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=email,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    messages.success(request, 'Register successifull. Log in here!!')
                    return redirect('login')
            else:
                messages.warning(request, 'Password must contain atleast 8 Characters')
                return redirect('register')
        else:
            messages.warning(request, 'Password missmatch')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Logged in successifully')
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Email or Password')
            return redirect('login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successifully')
    return redirect('/')

class ContactView(View):
    def get(self,*args,**kwargs):
        form = ReviewForm()
        context ={
            'form':form
        }
        return render(self.request,'contacts.html',context)
    
    def post(self,*args,**kwargs):
        form = ReviewForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            review = form.cleaned_data['review']
            rating = form.cleaned_data['rating']
            image = form.cleaned_data['profile_photo']

            reviews = Review(user=self.request.user,name=name,email=email,review=review,rating=rating,profile_photo=image)       
            reviews.save()
            messages.success(self.request, 'Review submitted successifully')
            return redirect('contact')
        else:    
            print(form.errors)
            messages.warning(self.request, 'Invalid form.')
            return redirect('contact')

class TripView(DetailView):
    model = Trip
    template_name = 'trips.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TripBookingForm()
        return context
     
    def post(self,*args,**kwargs):
        form = TripBookingForm(self.request.POST or None)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            adult = form.cleaned_data['adult']
            children = form.cleaned_data['children']
            date = form.cleaned_data['date']

            trip = Trip.objects.get(pk=kwargs['pk'])

            if form_validity([full_name,email,country,date]):              
                if TripBooking.objects.filter(user=self.request.user):
                    messages.warning(self.request, 'Failed!! You have an incomplete booking')
                    return redirect('trip',pk=kwargs['pk'])   

                trip_booking = TripBooking(
                    user=self.request.user,
                    full_name=full_name,
                    trip=trip,email=email,
                    country=country,
                    adult=adult,
                    children=children,
                    date=date)
                trip_booking.save()
                messages.success(self.request, 'Pay here to confirm your booking')
            else:
                messages.warning(self.request, "Please fill in the required fields to continue")
                return redirect('trip',pk=kwargs['pk'])
        
            payment_options = form.cleaned_data.get('payment_options')
            if payment_options == 'M':
                return redirect('tripmpesa')
            elif payment_options == 'P':
                return redirect('trippaypal')
            else:
                messages.warning(self.request, 'Invalid payment options')
            return redirect('trip',pk=kwargs['pk'])

        else:    
            print(form.errors)
            messages.warning(self.request, 'Select payment option to continue.')
            return redirect('trip',pk=kwargs['pk'])

class TripMpesaView(View):
    def get(self,*args,**kwargs):
        trip_bookings = TripBooking.objects.get(user=self.request.user)
        context = {
            'trip_bookings':trip_bookings,
        }  
        return render(self.request,'tripmpesa.html',context)      

class HotelMpesaView(View):
    def get(self,*args,**kwargs):
        hotel_bookings = HotelBooking.objects.get(user=self.request.user)
        context = {
            'hotel_bookings':hotel_bookings
        }  
        return render(self.request,'hotelmpesa.html',context) 

class TripPaypalView(View):
    def get(self,*args,**kwargs):
        trip_bookings = TripBooking.objects.get(user=self.request.user)
        context = {
            'trip_bookings':trip_bookings,
        }  
        return render(self.request,'trippaypal.html',context) 
    
class HotelPaypalView(View):
    def get(self,*args,**kwargs):
        hotel_bookings = HotelBooking.objects.get(user=self.request.user)
        context = {
            'hotel_bookings':hotel_bookings
        }  
        return render(self.request,'hotelpaypal.html',context) 

def paypal(request):
    return render(request,'paypal.html')   

class DestinationView(View):
    def get(self,*args,**kwargs):
        destination_list = Destination.objects.all()

        m = folium.Map(location=[-6.178061195803815, 35.749799646270844],zoom_start=6.3)

        for destination in destination_list:

            if destination.site == 'Game Park':
                folium.CircleMarker([destination.latitude, destination.longitude],
                    radius = 10,
                    color="white",
                    fill_color="blue",  
                    fill_opacity=0.7,
                    popup=f"<h6>{destination.title}</h6><img src='{destination.image.url}' width=200px height=120px >",
                    tooltip='GamePark click for more...').add_to(m)                
            elif destination.site == 'Museum': 
                folium.Marker([destination.latitude, destination.longitude],
                    popup=f"<h6>{destination.title}</h6><img src='{destination.image.url}' width=200px height=120px >",
                    tooltip='Musuem click for more...',
                    icon=folium.Icon(icon='glyphicon-home',icon_color='white',color='purple')).add_to(m)
            else:
                destination.site == 'Airport'
                folium.Marker([destination.latitude, destination.longitude],
                    popup=f"<h6>{destination.title}</h6><img src='{destination.image.url}' width=200px height=120px >",
                    tooltip='Airpot click for more...',
                    icon=folium.Icon(icon='glyphicon-plane',icon_color='darkred',color='red')).add_to(m)

        
        map_html = m._repr_html_()

        context={
            'm':map_html,
        }    

        return render(self.request,'destination.html',context)

class HotelView(View):
    def get(self,*args,**kwargs):
        hotel_list = Hotel.objects.all()
        
        m = folium.Map(location=[-6.178061195803815, 35.749799646270844],zoom_start=6.3)

        for hotel in hotel_list:
            custom_icon = CustomIcon("static/images/marker.png", icon_size=(40, 40))
            folium.Marker(
                location=[hotel.latitude, hotel.longitude],
                popup = f"<h6>{hotel.name}</h6><img src='{hotel.hotel_photo.url}' width=200px height=120px >",
                tooltip='Click for more...',
                icon=custom_icon).add_to(m)

            map_html = m._repr_html_()

        context={
            'm':map_html,
            'hotels':hotel_list
        }       
        return render(self.request,'hotels.html',context)

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hoteldetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['hotel_bookings'] = HotelBooking.objects.get(user=self.request.user)
        context['form'] = HotelBookingForm()
        return context
    
    def post(self,*args,**kwargs):
        form = HotelBookingForm(self.request.POST or None)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            period = form.cleaned_data['period']
            adult = form.cleaned_data['adult']
            children = form.cleaned_data['children']
            date = form.cleaned_data['date']

            hotel = Hotel.objects.get(pk=kwargs['pk'])

            if form_validity([full_name,email,date]):
                if HotelBooking.objects.filter(user=self.request.user):
                    messages.warning(self.request, 'Failed!! You have an incomplete hotel booking')
                    return redirect('hoteldetails',pk=kwargs['pk'])   

                hotel_booking = HotelBooking(
                    user=self.request.user,full_name=full_name,
                    hotel=hotel,email=email,period=period,adult=adult,
                    children=children,date=date)
                hotel_booking.save()
                messages.success(self.request, 'Done')
            else:
                messages.warning(self.request, "Please fill in the required fields to continue")
                return redirect('hoteldetails',pk=kwargs['pk'])  
                 
            payment_options = form.cleaned_data.get('payment_options')
            if payment_options == 'M':
                return redirect('hotelmpesa')
            elif payment_options == 'P':
                return redirect('hotelpaypal')
            else:
                messages.warning(self.request, 'Invalid payment options')
            return redirect('hoteldetails',pk=kwargs['pk'])
        

        else:    
            messages.warning(self.request, 'Invalid form.')
            return redirect('hoteldetails',pk=kwargs['pk'])


# def index(request):
#     cl = MpesaClient()
#     phone_number = '0700111222'
#     amount = 1
#     account_reference = 'reference'
#     transaction_desc = 'Description'
#     callback_url = 'https://api.darajambili.com/express-payment'
#     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#     return HttpResponse(response)        