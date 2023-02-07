from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy

from .models import ProductType, ProductSubType, Product, ProductCategory, PageHitCount


class MyAdminSite(AdminSite):
    site_title = gettext_lazy('BACKWOOD admin')
    site_header = gettext_lazy('BACKWOOD')
    index_title = gettext_lazy('Site administration')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
        'admin_image',
        'description',
    
    )
    readonly_fields = (
        'id',
        'slug',
        'absolute_url',
        'created_at',
        'updated_at',
    )
    list_editable = (
        'description',
    )


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
        'admin_image',
        'description',
    
    )
    readonly_fields = (
        'id',
        'slug',
        'absolute_url',
        'created_at',
        'updated_at',
    )
    list_editable = (
        'description',
    )


class ProductSubTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
        'description',
    )
    readonly_fields = (
        'id',
        'slug',
        'created_at',
        'updated_at',
    )
    
    list_editable = (
        'description',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'category',
        'is_active',
        'admin_image',
    )
    
    search_fields = (
        'name',
        'sku',
    )
    
    readonly_fields = (
        'id',
        'sku',
        'absolute_url',
        'slug',
        'created_at',
        'updated_at',
    )
    
    list_filter = (
        'category',
        'product_type',
        'product_sub_type',
        'colour',
        'quantity',
        'created_at',
        'updated_at',
    )
    
    list_per_page = 20


class PageHitCountAdmin(admin.ModelAdmin):
    list_display = (
        'url',
        'count',
    )
    search_fields = (
        'url',
    )
    readonly_fields = (
        'url',
        'count',
    )


admin.site = MyAdminSite()
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductSubType, ProductSubTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PageHitCount, PageHitCountAdmin)
