from django.shortcuts import render

from .cart import Cart
from store.models import Product #needed to find what item needs to be added to cart
from django.shortcuts import get_object_or_404 #as well for added to cart
from django.http import JsonResponse #to return json response

# Create your views here.

def cart_summary(request):
    #we want to get our cart session info
    cart = Cart(request)
    
    return render(request, 'cart/cart-summary.html', {'cart':cart})


def cart_add(request):
   
    cart = Cart(request) #so we create a cart object and pass in the request to see if it is a returning customer or new one
    if request.POST.get('action') == 'post':
        #if request from ajax is post then retrieve the data from our front end, product id and quantity
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity')) #grab variables from ajax

        #query, instance of object
        product = get_object_or_404(Product, id=product_id)

        #pass it to cart class through function
        cart.add(product=product, product_qty=product_quantity)

        #made so the return quantity for sum is current 
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})

        return response


def cart_delete(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id) #similar to cart.add

        #next make sure the quantity in cart is right after deleting product
        cart_quantity = cart.__len__()

        cart_total = cart.get_total()


        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response






def cart_update(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        
        product_quantity = int(request.POST.get('product_quantity')) #grab variables from ajax

        cart.update(product=product_id, qty=product_quantity)

        #next make sure the quantity in cart is right after deleting product
        cart_quantity = cart.__len__()

        cart_total = cart.get_total()

        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response