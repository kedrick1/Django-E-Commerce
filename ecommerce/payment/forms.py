
from django import forms 
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):

    class Meta:

        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'province', 'zip_code',] 
        #user is not there yet, we exclude it
        exclude = ['user',]

        

