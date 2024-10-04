from . cart import Cart #Cart class from cart file

def cart(request):
    
    return {'cart': Cart(request)} #return default data from initialized class, across all templates
    

