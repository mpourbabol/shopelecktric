from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.translation import gettext as _

from .filters import ProductFilter
from .forms import CommentForm
from .models import Comment, Product, Variants, Views


def home_view(request):
    qs = Product.objects.filter(available=True)
    return render(request, 'home/home.html', {
        'all_products': qs.order_by('-create')[:8],
        'new_arrivals': qs.order_by('-create')[:8],
        'featured_products': qs.filter(discount__gt=0).order_by('-sell')[:8] or qs.order_by('-num_view')[:8],
        'top_selling': qs.order_by('-sell', '-num_view')[:8],
    })


def product_list_view(request):
    products = Product.objects.filter(available=True).order_by('-create')
    product_filter = ProductFilter(request.GET, queryset=products)
    paginator = Paginator(product_filter.qs, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'home/product_list.html', {
        'filter': product_filter,
        'page_obj': page_obj,
        'products': page_obj,
    })


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    product.num_view += 1
    product.save(update_fields=['num_view'])

    ip = request.META.get('REMOTE_ADDR', '')
    Views.objects.create(
        product=product,
        user=request.user if request.user.is_authenticated else None,
        ip=ip,
    )

    comments = Comment.objects.filter(product=product, is_reply=False).select_related('user')
    variants = Variants.objects.filter(product_variant=product)
    is_favourite = (
        request.user.is_authenticated
        and product.favourite.filter(pk=request.user.pk).exists()
    )

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, _('Your comment has been posted.'))
            return redirect('home:product_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'home/product_detail.html', {
        'product': product,
        'variants': variants,
        'comments': comments,
        'form': form,
        'is_favourite': is_favourite,
    })


def search_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(available=True)
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(brand__name__icontains=query)
        ).distinct()
    paginator = Paginator(products.order_by('-create'), 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'home/search.html', {
        'query': query,
        'page_obj': page_obj,
        'products': page_obj,
    })


@login_required
def favourite_toggle_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.favourite.filter(pk=request.user.pk).exists():
        product.favourite.remove(request.user)
        product.total_favourite = max(0, product.total_favourite - 1)
        messages.info(request, _('Removed from favourites.'))
    else:
        product.favourite.add(request.user)
        product.total_favourite += 1
        messages.success(request, _('Added to favourites.'))
    product.save(update_fields=['total_favourite'])
    next_url = request.GET.get('next', 'home:home')
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(next_url)
