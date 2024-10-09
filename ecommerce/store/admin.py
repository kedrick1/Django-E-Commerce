from django.contrib import admin

from . models import Category, Product
# Register your models here.

# admin.site.register(Category)
# admin.site.register(Product)

#In Django's admin interface, @admin.register is a decorator that simplifies the process of registering models with the admin site. It’s a more modern and concise way to register models compared to the traditional method of using admin.site.register.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #we want to make use of a pre populated field
    #ex slug field automatically populate once i type name of category
    prepopulated_fields = {'slug': ('name',)}
    #When a new Category instance is created and the name field is filled in, the slug field will automatically be populated with a slugified version of the name.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('title',)}