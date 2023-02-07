from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
	path('checkout/', views.OrderCheckoutView.as_view(extra_context={'title': 'Checkout'}), name='checkout'),
]
