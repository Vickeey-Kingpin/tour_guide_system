from django import forms

PAYMENT_OPTIONS = (
    ('P','Paypal'),
    ('M','Mpesa')
)

class ReviewForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    review = forms.CharField()
    rating = forms.IntegerField()
    profile_photo = forms.ImageField(
        label='Profile photo',
        widget=forms.ClearableFileInput(attrs={
            'class':'image'
        }))
    
class TripBookingForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    country = forms.CharField(required=False)
    adult = forms.IntegerField(required=False)
    children = forms.IntegerField(required=False)
    date = forms.DateField(required=False)
    payment_options = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTIONS)

class HotelBookingForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    period = forms.IntegerField(required=False)
    adult = forms.IntegerField(required=False)
    children = forms.IntegerField(required=False)
    date = forms.DateField(required=False)
    payment_options = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTIONS)