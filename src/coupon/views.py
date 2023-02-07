from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupon.forms import CouponApplyForm
from coupon.models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    if form.is_valid():
        
        code = form.cleaned_data['code']
        coupon = get_object_or_404(Coupon, code__iexact=code,
                                   valid_from__lte=now,
                                   valid_to__gte=now,
                                   active=True)
        request.session['coupon_id'] = coupon.id
        messages.success(request, 'You have successfully applied the coupon!')
        return render(request, 'cart/messages.html')
    

