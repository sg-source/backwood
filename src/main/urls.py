import datetime

from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainView.as_view(extra_context={'title': 'Home'}), name='index'),
    path('shop/', views.ProductsListView.as_view(extra_context={'title': 'Products',
                                                            'no_products_msg': 'We didn\'t find anything \
                                                            on your request...'}),
         name='shop'),
    path('shop/<slug:slug>', views.ProductsListView.as_view(extra_context={'title': 'Products'}), name='shop'),
    path('shop/new/', views.NewProductsList.as_view(extra_context={'title': 'New Products'}), name='shop_new'),
    path('shop/new/<slug:slug>', views.NewProductsList.as_view(extra_context={'title': 'Products',
                                                                              'no_products_msg': 'Last 3 months \
                                                                              there have been no new products \
                                                                              in this category...'}),
         name='shop_new'),
    
    path('shop/sale/', views.DiscountedProductsList.as_view(extra_context={'title': 'Discounted Products',
                                                                           'no_products_msg': "There aren't any \
                                                                           products with discount"
                                                                           }),
         name='shop_sale'),
    
    path('products/<slug:slug>', views.ProductDetailsView.as_view(), name='product_detail'),
    path('about/', views.AboutView.as_view(extra_context={'title': 'About Us'}), name='about'),
    path('contact/', views.ContactView.as_view(extra_context={'title': 'Our Contacts'}), name='contact'),
    path('search/', views.SearchProductsView.as_view(), name='search'),
]

