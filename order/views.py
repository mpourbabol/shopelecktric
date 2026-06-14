from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from cart.models import Cart
from order.models import Coupon, ItemOrder, Order


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product', 'variant')
    if not cart_items.exists():
        messages.warning(request, _('Your cart is empty.'))
        return redirect('cart:cart_detail')

    total = sum(item.total_price for item in cart_items)
    coupon_discount = request.session.get('coupon_discount', 0)
    grand_total = total - (total * coupon_discount // 100) if coupon_discount else total

    if request.method == 'POST':
        user = request.user
        order = Order.objects.create(
            user=user,
            email=user.email,
            f_name=user.f_name or user.username,
            l_name=user.l_name or '',
            address=user.address or _('No address provided'),
            discount=coupon_discount or None,
        )
        for item in cart_items:
            ItemOrder.objects.create(
                order=order,
                user=user,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
            )
            product = item.product
            product.sell += item.quantity
            if item.variant:
                item.variant.amount = max(0, item.variant.amount - item.quantity)
                item.variant.save(update_fields=['amount'])
            else:
                product.amount = max(0, product.amount - item.quantity)
            product.save(update_fields=['sell', 'amount'])

        cart_items.delete()
        request.session.pop('coupon_code', None)
        request.session.pop('coupon_discount', None)
        messages.success(request, _('Order created successfully.'))
        return redirect('order:payment', order_id=order.id)

    return render(request, 'order/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'coupon_discount': coupon_discount,
        'grand_total': grand_total,
    })


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'order/payment.html', {
        'order': order,
        'zarinpal_sandbox': settings.ZARINPAL_SANDBOX,
    })


@login_required
@require_POST
def mark_paid_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order.paid = True
    order.save(update_fields=['paid'])
    messages.success(request, _('Payment confirmed. Thank you for your order!'))
    return redirect('order:order_detail', order_id=order.id)


@login_required
def zarinpal_stub_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    messages.info(
        request,
        _('Zarinpal sandbox: payment would be processed here. Mark as paid to continue.'),
    )
    return redirect('order:payment', order_id=order.id)


def payment_callback_view(request):
    messages.info(request, _('Payment callback received (sandbox stub).'))
    return redirect('order:order_list')


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-create')
    return render(request, 'order/order_list.html', {'orders': orders})
