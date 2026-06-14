from django.db.models import Count

from cart.models import Cart
from home.models import Category, Product


def electro_layout(request):
    categories = (
        Category.objects.filter(sub_cat=False)
        .annotate(product_count=Count('product'))
        .order_by('name')
    )
    sidebar_featured = Product.objects.filter(available=True).order_by('-sell')[:3]
    cart_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).select_related('product', 'variant')
        cart_total = sum(item.total_price for item in cart_items)
    return {
        'nav_categories': categories,
        'sidebar_featured': sidebar_featured,
        'cart_total': cart_total,
    }
