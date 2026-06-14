from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from home.models import Product, Variants


class Coupon(models.Model):
    code = models.CharField(_('Code'), max_length=100, unique=True)
    active = models.BooleanField(_('Active'), default=False)
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    discount = models.IntegerField(_('Discount'))

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.start <= now <= self.end


class Order(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    email = models.EmailField()
    f_name = models.CharField(max_length=300)
    l_name = models.CharField(max_length=300)
    address = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order #{self.id} - {self.user}'

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.order_item.all())

    @property
    def total_price(self):
        total = self.subtotal
        if self.discount:
            total -= total * self.discount // 100
        return total


class ItemOrder(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_item', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def unit_price(self):
        if self.variant:
            return self.variant.final_price
        return self.product.final_price

    @property
    def total_price(self):
        return self.unit_price * self.quantity
