from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    #admin url
    path('admin/', admin.site.urls),
    #store app
    path('', include('store.urls')),
    #cart app
    path('cart/', include('cart.urls')), #all url will start with cart/
    #account app
    path('account/', include('account.urls')),
]

#This setup allows Django to serve media files from the MEDIA_ROOT directory when MEDIA_URL is requested.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
