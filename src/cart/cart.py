import copy
from decimal import Decimal

from backwood import settings_base as settings
from coupon.models import Coupon
from main.models import Product
from main.exceptions import ProductOutOfStockError, MaxCartItemError


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart: dict[str, dict] = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart: dict[str, dict] = cart
        self.coupon_id: str = self.session.get('coupon_id')
        self.shipping = False
    
    def __repr__(self):
        return str(self.cart)
    
    def __getitem__(self, item: str):
        if item:
            return self.cart[item]
        raise ValueError("This element doesn't exist in the dict")
    
    def __iter__(self):
        products = Product.active_objects.filter(pk__in=self.cart.keys()).distinct().only(
            'absolute_url',
            'slug',
            'name',
            'price',
            'is_discount',
            'sum_discount',
            'image',
        
        )
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product: Product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(Decimal('{:.2f}'.format(product.get_total_price)))}

        item_quantity = 0 if override_quantity else int(self.cart[product_id]['quantity'])
        if product.quantity >= (item_quantity + quantity):
    
            if (item_quantity + quantity) > 10:
                
                raise MaxCartItemError('You cannot add more than 10 instances of the product to the cart')
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        else:
            raise ProductOutOfStockError('This product is no longer in stock in such quantity')
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    @property
    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item
                   in self.cart.values())
    
    def get_total(self):
        shipping = Decimal('{:.2f}'.format(15)) if self.shipping else Decimal('{:.2f}'.format(0))
        if self.coupon:
            return Decimal('{:.2f}'.format(self.get_subtotal - self.get_discount())) + shipping
        return self.get_subtotal + shipping
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return Decimal('{:.2f}'.format((self.coupon.discount / Decimal(100))
                                           * self.get_subtotal))
        return Decimal(0)
