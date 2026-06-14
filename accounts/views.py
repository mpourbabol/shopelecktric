from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from home.models import Product, Views

from .forms import CustomPasswordChangeForm, LoginForm, ProfileUpdateForm, RegistrationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailBackend')
            messages.success(request, _('Registration successful. Welcome!'))
            return redirect('home:home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user(), backend='accounts.backends.EmailBackend')
            messages.success(request, _('You are now logged in.'))
            next_url = request.GET.get('next', 'home:home')
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('home:home')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Password changed successfully.'))
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def favourites_view(request):
    products = request.user.fa_user.filter(available=True).order_by('-id')
    return render(request, 'accounts/favourites.html', {'products': products})


@login_required
def history_view(request):
    views = (
        Views.objects.filter(user=request.user)
        .select_related('product')
        .order_by('-create')
    )
    seen = set()
    unique_views = []
    for view in views:
        if view.product_id and view.product_id not in seen:
            seen.add(view.product_id)
            unique_views.append(view)
    return render(request, 'accounts/history.html', {'views': unique_views})
