from .cart import Cart


def cart(request):
	product_cart = Cart(request)
	return {'cart': product_cart, 'cart_len': len(Cart(request))}


