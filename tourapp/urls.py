from django.urls import path
from . views import *


urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout,name='logout'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('trip/<pk>/',TripView.as_view(),name='trip'),
    path('tripmpesa/',TripMpesaView.as_view(),name='tripmpesa'),
    path('hotelmpesa/',HotelMpesaView.as_view(),name='hotelmpesa'),
    path('trippaypal/',TripPaypalView.as_view(),name='trippaypal'),
    path('hotelpaypal/',HotelPaypalView.as_view(),name='hotelpaypal'),
    path('destinations/',DestinationView.as_view(),name='destinations'),
    path('hotels/',HotelView.as_view(),name='hotel'),
    path('hotel/<pk>/',HotelDetailView.as_view(),name='hoteldetails'),
]

