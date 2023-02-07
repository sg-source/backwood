from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
	path('checkout/', views.OrderCheckoutView.as_view(extra_context={'title': 'Checkout'}), name='checkout'),
	# path('invoice/', views.get_new_invoice, name='invoice'),
	# path('checkout/', views.order_checkout, name='checkout'),
]