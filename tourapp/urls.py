from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views


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

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='reset_password.html'),
        name='reset_password'),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'),
        name='password_reset_confirm'),
        
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
        name='password_reset_complete'),
]

