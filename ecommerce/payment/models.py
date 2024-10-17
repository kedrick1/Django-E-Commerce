from django.db import models

from django.contrib.auth.models import User #we want to know which user correlates to that shipping info,not required

# Create your models here.

class ShippingAddress(models.Model):

    #when sending form this must be entered
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    #optional
    province = models.CharField(max_length=255, null=True, blank=True) #not required, blank is client side?
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    #foreign key , user to match it so one for one 
    #authenticated vs non (bear in mind)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #if user is deleted then shipping info deleted as well, last two is because

    class Meta:
        verbose_name_plural = 'Shipping Address'  #so it is not addresss when registering model


    def __str__(self):
        return 'Shipping Address - ' + str(self.id) #so it is not shipping address (1) (2)





#shippimd model to hold shipping information so when proceed to checkout the fields will automatically fill in, just confirm payment, all this if user as account
