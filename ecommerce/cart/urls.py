
from django.urls import path
from . import views

urlpatterns = [

    #4 urls,one summary,adding deleting updating
    #will use asynchronosly with javascript
    path('', views.cart_summary, name='cart-summary'),

    #These three will not be actual url we can reach, they will be
    #handled using ajax which is asynchronous javascript
    path('add/', views.cart_add, name='cart-add'), #the name is referencing our url?
    path('delete/', views.cart_delete, name='cart-delete'),
    path('update/', views.cart_update, name='cart-update'),

    
]
















