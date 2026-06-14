from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from home.models import Product, Variants


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'{self.user} - {self.product}'

    @property
    def total_price(self):
        price = self.variant.final_price if self.variant else self.product.final_price
        return price * self.quantity


class Compare(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.product}'
