from django.shortcuts import render, redirect

from .forms import CreateUserForm

from payment.forms import ShippingForm #for the manage-shipping html , make query on shipping address model and push it with form
from payment.models import ShippingAddress #same as above

from django.contrib.auth.models import User

#for using the token
from django.contrib.sites.shortcuts import get_current_site #get our project, if hosted will collect domain name,since local not much 127...
from .token import user_tokenizer_generate
#these 3 are use for markup two above one down
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str #text dj3 str dj4
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode #decode token generator so its usable then encode to send

#for login
from django.contrib.auth.models import auth #allow use to do authentication
from django.contrib.auth import authenticate, login, logout #functions
from .forms import LoginForm , UpdateUserForm #not optimal but for clarity
from django.contrib.auth.decorators import login_required #decorators



from django.contrib import messages #django built in messages, where we can invoke it 


# Create your views here.

#so basically if user register then we will have all the info and we will create a link in the ver that will itself call the success
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        
        if form.is_valid():

           #override user object
           user = form.save()
           user.is_active = False #by default deactivated until token verif
           user.save()

           # email verif setup (email-verification.html)
           current_site = get_current_site(request)

           #subject heading for activation email
           subject = 'Account verification email'

           message = render_to_string('account/registration/email-verification.html', {
               
               'user': user,
               'domain': current_site, #so whether it is a local host or official domain
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': user_tokenizer_generate.make_token(user), #set token
               #we will transform verif template with following data

           }) #?why here this and not like before where url name

           #send email
           user.email_user(subject=subject, message=message)

           return redirect('email-verification-sent') #page to redirect
        
    context = {'form': form} #use this in html page

    return render(request, 'account/registration/register.html', context)




def email_verification(request, uidb64, token):
    
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id) #user based on unique_id

    #when user click on the email what page does he get
    #success

    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True

        user.save()

        return redirect('email-verification-success')
        

    #failed
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    
    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')
    

def email_verification_failed(request):
    
    return render(request, 'account/registration/email-verification-failed.html')



#so in steps
#1 user fills the register form
#2 we grab that form and instantiate as object, then set to false until activated
#3 then we grab all data and render it as string in email verification and create the link using the token and unique id and domain, uniquely generated link
#4 once done that, we send email to user and show the email was sent template
#5 email_verification function kick in and decode the url based on uid and grab user id and check if user click on link then activate them and redirect to right success or failed





#login
def my_login(request):
    
    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST) #collect all data from post request

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')
            #do authentication
            user = authenticate(request, username=username, password=password)

            if user is not None: #if user exist, login

                auth.login(request, user)

                return redirect("dashboard") #to dashboard
            
    
    context = {'form': form}

    return render(request, 'account/my-login.html', context=context)


#logout

def user_logout(request):

    auth.logout(request) #clear our session
    #problem we can have with just this is : make sure clear all sessions except the one of our cart

    ###will omite this code as i dont think it represent a real cart functionality

    # try:
    #     for key in list(request.session.keys()): #going through all keys
    #         if key == 'session_key':
    #             continue
    #         else:
    #             del request.session[key]
    # except KeyError:
    #     pass

    messages.success(request, "Logout success!") #will show on redirect page, so wherever we redirect thats where you must put the html template for messages
    
    return redirect("store") #return to home page

#Dashboard

@login_required(login_url='my-login') #unauthenticated user wont be able to access this dashboard, will send to login form
def dashboard(request):
    return render(request, 'account/dashboard.html')


#delete/profile
@login_required(login_url='my-login')
def profile_management(request):
    
    #updating our user's username and email

    user_form = UpdateUserForm(instance=request.user) #username verification, says if username is already used, best to put it before
    #if not there then will not show the validation error

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user) #capture all data, based on instance of the current user
        
        if user_form.is_valid():
            user_form.save()

            messages.info(request, "Account updated!")


            return redirect('dashboard') #if no issue go back to dashboard

    # user_form = UpdateUserForm(instance=request.user)

    context= {'user_form': user_form}

    return render(request, 'account/profile-management.html', context=context)


@login_required(login_url='account/delete-account.html')
def delete_account(request):
    
    user= User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()

        messages.error(request, "Account deleted!")

        return redirect('store')
    
    return render(request, 'account/delete-account.html')






#shipping view 
@login_required(login_url='my-login')
def manage_shipping(request):
    
    try:
        #account user with shipment information

        shipping = ShippingAddress.objects.get(user=request.user.id) #get id from active user and compare with the user field to see if has shipping field

    except ShippingAddress.DoesNotExist:

        #account user with no shipment information

        shipping = None 

    form = ShippingForm(instance=shipping) #wheter yes or no, if yes prefield the form with info , else clear form

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping) #posting to that specific instance

        if form.is_valid():

            # assign the user FK on the object

            shipping_user = form.save(commit=False) 

            #adding foreign key
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')
    
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)



#we query the database to see if we have an entry for the current user id and if so an instance of the model is created
#for example wed get a to get page, and then click to update shipping info sending a post request

