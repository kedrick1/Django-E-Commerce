from django.shortcuts import render
from . models import Category, Product

from django.shortcuts import get_object_or_404 #needed for product_info , so get object or show 404 error

# Create your views here.

def store(request):

    all_products = Product.objects.all()
    context = {'all_products': all_products} #first can be anything we want, just a key
    return render(request, 'store/store.html', context) #context=context) ,need the second store since not right in template


def categories(request):
    #query database, need model
    all_categories = Category.objects.all()
    return {'all_categories': all_categories} 
    #this we want all categories value to be available across all pages through the nav bar drop down search
    #to do this we need a context processor
    #In Django, context processors are Python functions that allow you to inject variables into the context of all 
    # templates. This is particularly useful for making certain data available globally without having to pass it 
    # explicitly in every view

    #no need to render it like usual since available to all


def list_category(request, category_slug=None):
    
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category': category, 'products': products})


#going to reference our slug and return necessary data, aka individual product from database
def product_info(request, product_slug): 
    #the slug is gotten from our url, its a extra param, and its gonna be send by clicking on the url name from the product card?
    product = get_object_or_404(Product, slug=product_slug) #get specific object where slug = slug and all are unique
    context = {'product': product}

    return render(request, 'store/product-info.html', context) 


