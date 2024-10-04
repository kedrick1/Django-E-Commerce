from decimal import Decimal
from store.models import Product

#all cart functionability will be
#session handling


class Cart():
    #will utilise request for our session
    def __init__(self, request) -> None:
        
        #if user is new to site then new session but if returning we need to get that old session/cookies
        self.session = request.session
        cart = self.session.get('session_key') 
        #if key is empty then we need to asign a session to that user, empty dictionnary
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} #self.session: Refers to an object that manages session data.
                                                    #['session_key']: This is a specific key in the session dictionary where you want to store the cart data.
                                                    #={}: Initializes this key with an empty dictionary.
        # Store a value in the session
        #self.session['key'] = 'value'

        # Retrieve a value from the session
        #value = self.session.get('key')

        self.cart = cart


    def add(self, product, product_qty):
        product_id = str(product.id) #since is a object instance

        if product_id in self.cart: #just modify quantity if cart already has item
            self.cart[product_id]['qty'] = product_qty
        else: #creates new entry in cart dictionnary
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        
        self.session.modified = True




    def delete(self, product):

        product_id = str(product)

        if product_id in self.cart:
            
            del self.cart[product_id] #already a string

        self.session.modified = True




    def update(self, product, qty):
        
        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:

            self.cart[product_id]['qty'] = product_quantity #checking cart for product and if so set the qty to the new one
        
        self.session.modified = True


    #new function to count all product we currently have in our session and render that function within template

    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())

    
    #this function help iterate through cart
    def __iter__(self):

        #get all product ids
        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)
        #In Django, id_in is typically used as a filter or lookup in a query to check if a specific field's value exists in a list of values
        import copy

        cart = copy.deepcopy(self.cart)
        #cart = self.cart.copy() #copy of session shallow instead of deep

        for product in products: #products is a list of all complete objects, compare to cart which only has qty and price, then you also had everything has a product key
            cart[str(product.id)]['product'] = product
            

        #before 
        # cart = {
        #             '1': {'price': '19.99', 'qty': 2},
        #             '2': {'price': '29.99', 'qty': 1}
        #     }
        #after
        # cart = {
        #         '1': {
        #         'price': '19.99', 
        #         'qty': 2, 
        #         'product': <Product object with attributes like title, image, etc.>
        #     },
        #         '2': {
        #         'price': '29.99', 
        #         'qty': 1, 
        #         'product': <Product object with attributes like title, image, etc.>
        #     }
        # }
        for item in cart.values(): #here its the after, each structure of value is the 3 pair key/value  , 

            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']
            #the yield statement is commonly used within generator functions to return a value without terminating the function
            yield item


    def get_total(self):

        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

















