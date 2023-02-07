from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.CartDetailView.as_view(extra_context={'title': 'My Cart'}), name='detail'),
	path('add/<int:product_id>/', views.CartUpdateView.as_view(), name='add'),
	path('remove/<int:product_id>/', views.CartRemoveView.as_view(), name='remove'),
	path('cart/', views.Minicart.as_view(), name='cart'),
]