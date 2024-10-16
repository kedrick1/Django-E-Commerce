#using django forms

#registration forms , default user creation form
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#login
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput #entering username and password input




# creating a user

class CreateUserForm(UserCreationForm): #can be named anything
    
    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2'] #pass2 is confirmation

    #we want to make sure that extra functionality to validate unique email , django already has some for username

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True #makes the email field required


#When a user submits a form, Django takes the raw data (usually from request.POST).
# Each field in your form goes through validation. If you have defined custom cleaning methods (like clean_email), they will be called during this process.
#The clean_<fieldname>() method for a specific field is called first, where you can perform field-specific validation.
#If the field passes validation, the cleaned value is added to self.cleaned_data.
#After all fields are validated, you can access the cleaned data dictionary (self.cleaned_data) to retrieve the validated values.

    # Email validation    
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.validationError('Already used email')
        
        #extra validation to check email length
        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long')
        
        return email 
    



# login in a user

class LoginForm(AuthenticationForm):
    #in form user input username and password
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    


#updating username and email form 
 
class UpdateUserForm(forms.ModelForm):

    password = None #not gonna use it

    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True #makes the email field required

    #email validation
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists(): #allow us to just keep the user email without having an issue, so if user email no exception raised else error
            raise forms.ValidationError('Already used email')
        
        #extra validation to check email length
        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long')
        
        return email 
