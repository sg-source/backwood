from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order')),
    path('coupon/', include('coupon.urls', namespace='coupon')),
    path('favourites/', include('favourites.urls', namespace='favourites')),
    
    path('__debug__/', include('debug_toolbar.urls')),
]

handler404 = "main.views.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
