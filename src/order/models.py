from django.db import models

from coupon.models import Coupon
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Product

from authapp.models import User

STATUS = (
    ('processing', 'processing'),
    ('awaiting payment', 'awaiting payment'),
    ('ready for getting', 'ready for getting'),
    ('delivered', 'delivered'),
    ('rejected', 'rejected')
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.SET_NULL,
                             related_name='orders', default=None,
                             null=True, blank=True)
    firstname = models.CharField(verbose_name='firstname', max_length=255)
    lastname = models.CharField(verbose_name='lastname', max_length=255)
    email = models.EmailField(verbose_name='email', db_index=True)
    phone = models.PositiveIntegerField(verbose_name='phone', default=None, blank=True, null=True)
    address = models.CharField(verbose_name='address', max_length=250, blank=True, null=True)
    postal_code = models.CharField(verbose_name='postal code', max_length=20, blank=True, null=True)
    city = models.CharField(verbose_name='city', max_length=100, blank=True, null=True)
    notes = models.TextField(verbose_name='notes', max_length=250, default=None)
    shipping = models.BooleanField(verbose_name='shipping', default=False, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, related_name='coupons', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    is_paid = models.BooleanField(verbose_name='is paid', default=False)
    status = models.CharField(max_length=40, choices=STATUS, blank=True, null=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_subtotal(self):
        return sum(item.get_cost() for item in self.orders.all())
    
    def get_total(self):
        return sum(item.get_cost() for item in self.orders.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity


@receiver(post_save, sender=OrderItem)
def update_the_product_quantity(sender, instance, **kwargs) -> None:
    product = Product.objects.get(id=instance.product.id)
    product.quantity = F('quantity') - instance.quantity
    product.save()

