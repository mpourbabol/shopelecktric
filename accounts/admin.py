from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .models import EmailToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'f_name', 'l_name', 'is_active', 'is_admin', 'create')
    list_filter = ('is_active', 'is_admin')
    search_fields = ('email', 'username', 'f_name', 'l_name')
    ordering = ('-create',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('f_name', 'l_name', 'phone', 'address', 'profile_image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(EmailToken)
class EmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    search_fields = ('user__email', 'token')
