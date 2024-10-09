from django.urls import path
from . import views

urlpatterns = [
    
    #store main page
     path('', views.store, name='store'),
     #individual product
     path('product/<slug:product_slug>/', views.product_info, name='product-info'),#url path for our individual product when selected, lug fields come into play,dynamic value
     #individual category, had error because no category_slug
     path('search/<slug:category_slug>/', views.list_category, name='list-category'),#url path for our individual product when selected, lug fields come into play,dynamic value

]




















