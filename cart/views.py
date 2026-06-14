from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from home.models import Product, Variants

from .models import Cart, Compare


def _get_compare_queryset(request):
    if request.user.is_authenticated:
        return Compare.objects.filter(user=request.user)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return Compare.objects.filter(session_key=session_key, user__isnull=True)


@login_required
def cart_detail_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product', 'variant')
    total = sum(item.total_price for item in cart_items)
    coupon_discount = request.session.get('coupon_discount', 0)
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
        'coupon_discount': coupon_discount,
        'grand_total': total - (total * coupon_discount // 100) if coupon_discount else total,
    })


@login_required
@require_POST
def cart_add_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    variant = None
    if variant_id:
        variant = get_object_or_404(Variants, pk=variant_id, product_variant=product)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        variant=variant,
        defaults={'quantity': quantity},
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    messages.success(request, _('Product added to cart.'))
    next_url = request.POST.get('next', 'cart:cart_detail')
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(next_url)


@login_required
@require_POST
def cart_remove_view(request, item_id):
    cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)
    cart_item.delete()
    messages.info(request, _('Item removed from cart.'))
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_update_view(request, item_id):
    cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        cart_item.delete()
        messages.info(request, _('Item removed from cart.'))
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, _('Cart updated.'))
    return redirect('cart:cart_detail')


@login_required
@require_POST
def apply_coupon_view(request):
    from order.models import Coupon

    code = request.POST.get('code', '').strip().upper()
    try:
        coupon = Coupon.objects.get(code__iexact=code)
        if coupon.is_valid():
            request.session['coupon_code'] = coupon.code
            request.session['coupon_discount'] = coupon.discount
            messages.success(request, _('Coupon applied successfully.'))
        else:
            messages.error(request, _('This coupon is not valid.'))
    except Coupon.DoesNotExist:
        messages.error(request, _('Invalid coupon code.'))
    return redirect('cart:cart_detail')


def compare_view(request):
    compare_items = _get_compare_queryset(request).select_related('product', 'product__brand')
    products = [item.product for item in compare_items[:4]]
    return render(request, 'cart/compare.html', {'products': products})


@require_POST
def compare_add_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)
    compare_qs = _get_compare_queryset(request)
    if compare_qs.count() >= 4:
        messages.error(request, _('You can compare up to 4 products.'))
        return redirect(request.POST.get('next', 'cart:compare'))

    if request.user.is_authenticated:
        Compare.objects.get_or_create(user=request.user, product=product)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        Compare.objects.get_or_create(
            session_key=session_key, user=None, product=product
        )
    messages.success(request, _('Product added to compare list.'))
    next_url = request.POST.get('next', 'cart:compare')
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(next_url)


@require_POST
def compare_remove_view(request, product_id):
    compare_qs = _get_compare_queryset(request)
    compare_qs.filter(product_id=product_id).delete()
    messages.info(request, _('Product removed from compare list.'))
    return redirect('cart:compare')
