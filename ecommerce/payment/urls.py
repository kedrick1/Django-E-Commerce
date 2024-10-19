from django.urls import path
from . import views


urlpatterns = [

    path('payment-success', views.payment_succes, name='payment-success'),
    path('payment-failed', views.payment_failed, name='payment-failed'),
    path('checkout', views.checkout, name='checkout'),
    path('complete-order', views.complete_order, name='complete-order')
]




#shippimd model to hold shipping information so when proceed to checkout the fields will automatically fill in, just confirm payment, all this if user as account


