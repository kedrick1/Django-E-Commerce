from django.db import models

from django.urls import reverse #imported to create own url for dynamic links?
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True) #set to true, helps with query acceleration/memory usage/faster look up in table
    slug = models.SlugField(max_length=255, unique=True)
    #similar to route, /shoes /shirts this is slug field /shoes/nike-air-jordan

    class Meta:
        verbose_name_plural = 'categories' #when register it, makes it plural so override with categories

    def __str__(self):
        return self.name #in admin wed see category (1), now with this will show the actual name attribute, so shoe or shirt
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])
    
        
class Product(models.Model):

    #FK
    category= models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='un-branded')
    description = models.TextField(blank=True) #bigger text needed , blank means optional can be blank
    slug = models.SlugField(max_length=255) #all product are unique so we have slug,
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/') #later we have media folder named images with what picture to use
    #whenever we have image uploaded it will go to the images/ folder
    #we installed pillow to work with this

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title #in admin wed see product (1), now with this will show the actual title attribute, so shoe or shirt
    
    #create dynamic url
    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse
        return reverse('product-info', args=[self.slug])
        #kwargs={'pk': self.pk}) #the name is from the path name value