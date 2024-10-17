from django.urls import path
from . import views


urlpatterns = [

    path('payment-success', views.payment_succes, name='payment-success'),
    path('payment-failed', views.payment_failed, name='payment-failed'),
    path('checkout', views.checkout, name='checkout'),
]




#shippimd model to hold shipping information so when proceed to checkout the fields will automatically fill in, just confirm payment, all this if user as account


