from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import DeletionMixin, ProcessFormView, FormMixin

from coupon.forms import CouponApplyForm
from main.models import Product
from rest_framework.response import Response
from rest_framework.views import APIView
from .cart import Cart
from .forms import CartAddProductForm
from main.exceptions import ProductOutOfStockError, MaxCartItemError


@method_decorator(require_POST, name='dispatch')
class CartUpdateView(FormMixin, ProcessFormView):
    form_class = CartAddProductForm
    
    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super().setup(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        
        pk = kwargs.get('product_id')
        product = get_object_or_404(Product, pk=pk)
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            try:
                self.cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
            except ProductOutOfStockError as out_of_stock_err:
                return JsonResponse(data={'err': str(out_of_stock_err)})
            
            except MaxCartItemError as max_item_cart_err:
                return JsonResponse(data={'err': str(max_item_cart_err)})
            
            if 'get_total' in form.data:
                cart_subtotal = self.cart.get_subtotal
                cart_total = self.cart.get_total()
                product_total_price = Decimal(self.cart[str(product.pk)]['price']) * self.cart[str(product.pk)][
                    'quantity']
                return JsonResponse(data={'id': product.pk,
                                          'cart_total': Decimal(cart_total),
                                          'cart_subtotal': Decimal(cart_subtotal),
                                          'get_discount': self.cart.get_discount() if self.cart.coupon else None,
                                          'product_total_price': product_total_price}, status=200)
            
            location = request.POST.get('location')
            if location and location == '/':
                return render(request, 'main/includes/header_actions.html')
            return render(request, 'main/includes/header.html')

        return JsonResponse(data={'err': 'It is impossible to add the product to the cart'})
    
    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.update(request, *args, **kwargs)


@method_decorator(require_POST, name='dispatch')
class CartRemoveView(DeletionMixin, View):
    
    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super().setup(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if self.cart:
            pk = self.kwargs.get('product_id')
            if pk is not None:
                product = get_object_or_404(Product, pk=pk)
                self.cart.remove(product)
                
                if 'cart_total_price' in request.POST and bool(request.POST['cart_total_price']) is not False:
                    if self.cart:
                        return JsonResponse({'cart_total_price': self.cart.get_total()})
                    else:
                        empty_cart = render_to_string('cart/includes/empty-cart.html')
                        return JsonResponse({'cart': 'empty', 'empty_cart': empty_cart})
                
                if request.POST['location'] and request.POST['location'] != '/':
                    return render(request, 'main/includes/header.html')
                return render(request, 'main/includes/header_actions.html')


class CartDetailView(FormMixin, TemplateView):
    form_class = CartAddProductForm
    template_name = 'cart/cart.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({'override': True})
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupon_apply_form = CouponApplyForm()
        context['coupon_apply_form'] = coupon_apply_form
        return context
    
    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if not self.cart:
            return redirect('main:shop')
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'total': str(self.cart.get_total()),
                                 'get_discount': str(self.cart.get_discount()),
                                 'discount': str(self.cart.coupon.discount) if self.cart.coupon else 0,
                                 'subtotal': str(self.cart.get_subtotal)})
        
        return super().get(request, *args, **kwargs)


class Minicart(APIView):
    queryset = Product.active_objects.all()
    
    def get(self, request):
        context = dict()
        context['cart'] = Cart(request)
        context.update(csrf(request))
        minicart = render_to_string('main/includes/minicart.html', context)
        return Response(minicart)
