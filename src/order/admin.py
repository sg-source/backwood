from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']


# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'firstname', 'lastname',
					'email', 'phone', 'city', 'address',
					'postal_code', 'is_paid', 'status',
					'created', 'updated']
	list_filter = ['is_paid', 'created', 'updated']
	inlines = [OrderItemInline]
	

admin.site.register(Order, OrderAdmin)
