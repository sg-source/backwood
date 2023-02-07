from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from django.views.generic.edit import ModelFormMixin, CreateView

from coupon.forms import CouponApplyForm
from .models import OrderItem, Order
from .forms import OrderCreateForm, PaymentForm
from cart.cart import Cart


class OrderCheckoutView(CreateView):
    template_name = 'order/checkout.html'
    form_class = OrderCreateForm
    model = Order
    
    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if not self.cart:
            return redirect('main:shop')
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'total': str(self.cart.get_total()),
                                 'get_discount': str(self.cart.get_discount()),
                                 'discount': str(self.cart.coupon.discount),
                                 'total_price': str(self.cart.get_subtotal)})
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            self.is_paid = self.make_payment(data=payment_form.cleaned_data)
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.POST['shipping']:
            self.request.session.modified = True
            self.cart.shipping = True if request.POST.get('shipping') == 'True' else False
            return JsonResponse({'total': str(self.cart.get_total()),
                                 'get_discount': str(self.cart.get_discount()),
                                 'discount': str(self.cart.coupon.discount) if self.cart.coupon else 0,
                                 'total_price': str(self.cart.get_subtotal)})
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = PaymentForm
        context['coupon_apply_form'] = CouponApplyForm
        
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({'shipping': False})
        if self.request.user.is_authenticated:
            initial.update({'firstname': self.request.user.firstname.capitalize(),
                            'lastname': self.request.user.lastname.capitalize() if self.request.user.lastname else None,
                            'email': self.request.user.email.lower() if self.request.user.email else None,
                            'phone': self.request.user.phone if self.request.user.phone else None}
                           )
        
        return initial
    
    def get_success_url(self):
        return self.request.path
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id if self.request.user.is_authenticated else None
        self.object.save()
        for item in self.cart:
            OrderItem.objects.create(
                order=self.object,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        self.cart.clear()
        self.request.session.pop('coupon_id', None)
        
        if self.is_paid:
            self.object.is_paid = True
            self.object.status = 'processing'
            self.object.save()
            
            data = {
                'order': self.object,
                'order_items': self.object.orders.all(),
                'title': 'Invoice',
            }
            print(data['order_items'])
            return render(self.request, 'order/invoice.html', context=data)
        
        return super(ModelFormMixin, self).form_valid(form)
    
    def make_payment(self, data=None):
        """Some kind of payment logic. Just for example"""
        self.payment_data = data
        return True
