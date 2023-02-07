import datetime
import random
from copy import copy, deepcopy
from itertools import chain

from urllib.parse import parse_qsl

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, F, Count, Value as V, Case, When, CharField, DecimalField
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_safe, require_GET
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ContactForm
from .models import ProductType, ProductCategory, Product, COLOURS, PageHitCount, \
    DISCOUNTS, NEW_PRODUCTS_DELTA_DAYS
from cart.forms import CartAddProductForm
from .serializers import SearchProductsSerializer, SearchCategoriesSerializer, SearchTypesSerializer
from .recently_viewed import RecentlyViewedProducts


AD_BLOCKS_PRODUCTS_NUMBER = 8


@method_decorator(require_safe, name='dispatch')
class MainView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        discounts_values = [i[0] for i in DISCOUNTS]
        
        context = super().get_context_data(**kwargs)
        
        categories_and_types = ProductCategory.active_objects \
            .annotate(entity=V('category')).values(
                'name',
                'slug',
                'absolute_url',
                'entity', ) \
            .union(ProductType.active_objects.annotate(entity=V('product type')).values(
                'name',
                'slug',
                'absolute_url',
                'entity', )
        )
        
        # It is supposed that ad block 'Special offer:new' displays new products (whose age is 180 days for ex.),
        # but this is a test QuerySet for illustration. Likewise, the same QuerySet will be in 'Special offer:featured'
        # & 'Special offer:top'. The same goes for the lower block 'Be Sure To Watch This'
        special_new_queryset = Product.active_objects.miniproduct.filter(
            Q(created_at__gte=datetime.datetime.today() - datetime.timedelta(days=NEW_PRODUCTS_DELTA_DAYS)) &
            Q(created_at__lte=datetime.datetime.today()))[:8]

        # That's because of a special html output
        special_new = [(special_new_queryset[i], special_new_queryset[i + 1]) for i in
                       range(0, len(special_new_queryset), 2)]

        special_sale = Product.active_objects.miniproduct.filter(sum_discount__in=discounts_values)[:4] \

        # TODO order_by in Postgres(doesn't work with union in SQLite)
        random_categories_and_types = ProductCategory.active_objects.values('name', 'image', 'absolute_url') \
                                          .annotate(count=Count('product')) \
                                          .annotate(count=Count('absolute_url')) \
                                          .union(
            ProductType.active_objects.values('name', 'image', 'absolute_url')
            .annotate(count=Count('product'))
            .annotate(count=Count('absolute_url'))
        )[:6]
        
        # The same goes for the lower block 'Be Sure To Watch This'
        bottom_recommended = Product.active_objects.miniproduct.exclude(
            Q(id__in=special_new_queryset.values('id')) &
            Q(id__in=special_sale.values('id'))).order_by('?')[:8]
        
        context['categories_and_types'] = categories_and_types
        context['random_categories_and_types'] = random_categories_and_types
        context['special_new'] = special_new
        context['special_sale'] = special_sale
        context['bottom_recommended'] = bottom_recommended

        return context


class ProductsListView(ListView):
    filtered = {}
    qs = []
    model = Product
    queryset = Product.active_objects.get_products_for_main_filter()
    template_name = 'main/shop.html'
    context_object_name = 'products'
    paginate_by = 12
    is_filter = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_and_types'] = ProductCategory.active_objects \
            .annotate(entity=V('category')).values(
            'name',
            'slug',
            'absolute_url',
            'entity', ) \
            .union(ProductType.active_objects.annotate(entity=V('product type')).values(
            'name',
            'slug',
            'absolute_url',
            'entity', )
        )
        
        context['filtered'] = self.filtered
        context['colours'] = {item: dict(COLOURS).get(item)
                              for item in Product.active_objects.values_list('colour', flat=True).distinct()}
        return context
    
    def get(self, request, *args, **kwargs):
        """Filtering products if there is parameters in ajax request"""
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            self.qs.clear()
            categories = []
            types = []
            colors = []
            price = []
            if request.GET:
                for filter_subject in dict(request.GET):
                    parse_data = parse_qsl(dict(request.GET)[filter_subject][0])
                    if dict(request.GET)[filter_subject][0] and filter_subject == 'categories':
                        
                        for item in parse_data:
                            if item[1] == 'category':
                                categories.append(item[0])
                            
                            elif item[1] == 'product type':
                                types.append(item[0])
                    
                    if dict(request.GET)[filter_subject][0] and filter_subject == 'colours':
                        for item in parse_data:
                            colors.append(item[0].upper())
                    
                    if dict(request.GET)[filter_subject][0] and filter_subject == 'price':
                        for item in dict(request.GET)[filter_subject][0].replace('$', '').split('-'):
                            price.append(int(item))
                    
                    self.filtered['categories'] = categories
                    self.filtered['types'] = types
                    self.filtered['colors'] = colors
                    self.filtered['price'] = price
                else:
                    if self.filtered:
                        self.is_filter = True
                        request.session['filtered'] = self.filtered
                        request.session.modified = True
            
            else:
                self.filtered.clear()
                request.session.pop('filtered', None)
                request.session.modified = True
            
            if categories and not types:
                self.queryset = Product.active_objects.get_products_for_main_filter() \
                    .filter(Q(category__name__in=categories))
            
            elif types and not categories:
                self.queryset = Product.active_objects.get_products_for_main_filter() \
                    .filter(Q(product_type__name__in=types))
            
            elif categories and types:
                self.queryset = Product.active_objects.get_products_for_main_filter() \
                    .filter(Q(category__name__in=categories) &
                            Q(product_type__name__in=types))
            
            self.template_name = 'main/includes/products_list.html'
            
            if colors:
                qs = self.queryset
                self.queryset = qs.filter(Q(colour__in=colors))
            
            if price:
                qs = self.queryset
                self.queryset = qs.filter(Q(price__gte=price[0]), Q(price__lte=price[1]))
            
            self.qs.append(self.queryset.values_list('pk', flat=True))
            
            return super().get(request, *args, **kwargs)
        else:
            if specific_category_or_type := kwargs.get('slug'):
                self.qs.clear()
                self.filtered.clear()
                request.session.pop('filtered', None)
                res = []
                try:
                    category = ProductCategory.active_objects.get(Q(slug=specific_category_or_type)).name
                except ProductCategory.DoesNotExist:
                    product_type = ProductType.objects.get(slug=specific_category_or_type, is_active=True).name
                    res.append(product_type)
                else:
                    res.append(category)
                self.filtered['categories'] = res
                self.queryset = Product.active_objects.get_products_for_main_filter() \
                    .filter(Q(product_type__name=res[0]) | Q(category__name=res[0]))
                self.qs.append(self.queryset.values_list('pk', flat=True))
            
            if any(self.qs):
                self.queryset = Product.active_objects.get_products_for_main_filter() \
                    .filter(Q(pk__in=self.qs[0]))
            return super().get(request, *args, **kwargs)


class NewProductsList(ProductsListView):
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        current_date = datetime.datetime.today()
        start_date = current_date - datetime.timedelta(days=NEW_PRODUCTS_DELTA_DAYS)
        self.queryset = Product.active_objects.get_products_for_main_filter().\
            filter(Q(created_at__gte=start_date) & Q(created_at__lte=current_date))
        
        return super(ProductsListView, self).get(request, *args, **kwargs)


class DiscountedProductsList(ProductsListView):
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.queryset = Product.active_objects.get_products_for_main_filter().\
            filter(Q(is_discount=True))
        
        return super(ProductsListView, self).get(request, *args, **kwargs)


class ProductDetailsView(FormMixin, DetailView):
    queryset = Product.active_objects.get_certain_product()
    model = Product
    form_class = CartAddProductForm
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    
    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and 'slug' in kwargs:
            product = get_object_or_404(Product, slug=kwargs['slug'])
            return render(request, 'main/includes/miniproduct.html', {'product': product})
        
        else:
            obj, created = PageHitCount.objects.get_or_create(url=request.path)
            obj.count = F('count') + 1
            obj.save()
            
            return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        recently_viewed = RecentlyViewedProducts(self.request)
        recently_viewed.update(int(self.object.id))
        
        recommended_products = Product.active_objects.miniproduct.filter(
            Q(category=self.object.category) |
            Q(product_type=self.object.product_type)).exclude(
            pk=self.object.id).order_by('?')[:5]
        
        
        obj = self.object.sum_discount
        
        context['recommended_products'] = recommended_products
        context['title'] = self.object.name
        
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'


class ContactView(ProcessFormView, FormMixin, TemplateView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({'firstname': self.request.user.firstname.capitalize(),
                            'email': self.request.user.email.lower() if self.request.user.email else None,
                            'phone': self.request.user.phone if self.request.user.phone else None}
                           )
        
        return initial
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Your letter has been sent. We will definitely contact you soon.')
            return render(request, 'main/includes/messages.html')
        else:
            return self.form_invalid(form)


@method_decorator(require_GET, name='dispatch')
class SearchProductsView(APIView):
    queryset = Product.objects.all()
    
    def get(self, request):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            products = self.queryset.filter(Q(sku=request.GET['data']) | Q(name__istartswith=request.GET['data']))
            categories = ProductCategory.active_objects.filter(Q(name__istartswith=request.GET['data']))
            types = ProductType.objects.filter(Q(name__istartswith=request.GET['data']))
            
            serializer_products = SearchProductsSerializer(products, many=True)
            serializer_categories = SearchCategoriesSerializer(categories, many=True)
            serializer_types = SearchTypesSerializer(types, many=True)
            
            return Response(
                dict(products=serializer_products.data,
                     categories=serializer_categories.data,
                     types=serializer_types.data,
                     )
            )
        return HttpResponseNotFound()
    
    
def page_not_found(request, exception):
    if request.GET['page']:
        return redirect('main:shop')
    raise Http404
