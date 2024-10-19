from django.shortcuts import render
from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.http import JsonResponse

# Create your views here.


def checkout(request):

    # Users with account -- pre-filled form
    if request.user.is_authenticated:

        try:
            #authenticated user with shipping information 
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context=context)
        
        except:
            #authenticated user without shipping information
            return render(request, 'payment/checkout.html')
        

    #guess user
    return render(request, 'payment/checkout.html')

def payment_succes(request):

    #clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]  #when we create cart session thats the key so delete cart instance?

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')


def complete_order(request):

    #check if request from ajax is post
    if request.POST.get('action') == 'post':
        #grab data 
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        province = request.POST.get('province')
        zipcode = request.POST.get('zipcode')

        #all in one shipping address for order object
        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + province + '\n' + zipcode)

        #shopping cart information, need import
        cart = Cart(request)

        #get total price of items, stored in amount paid in order object
        total_cost = cart.get_total()

        '''
            Order variations
            1) create order -> account user WITH + WITHOUT shipping information

            2) create order -> for guess users
        
        '''

        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
            #now order item, take order item as foreign key,
            order_id = order.pk #get primary key of this order and pass it as foreign key to order item

            for item in cart:

                #create an order item list for each item
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user)

        else:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)
            
            order_id = order.pk 

            for item in cart:

                OrderItem.object.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user) 

        order_success= True
        response = JsonResponse({'success': order_success})

        return response