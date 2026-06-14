from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Brand(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(_('Color'), max_length=200)

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(_('Trim'), max_length=100)

    class Meta:
        verbose_name = _('Trim')
        verbose_name_plural = _('Trims')

    def __str__(self):
        return self.name


class Category(models.Model):
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(_('Name'), max_length=200, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    sub_category = models.ForeignKey(
        'self', related_name='sub', blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name or ''


class Product(models.Model):
    STATUS_CHOICES = [
        ('None', 'None'),
        ('Size', 'Trim'),
        ('Color', 'Color'),
    ]

    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0)
    unit_price = models.PositiveBigIntegerField(default=0)
    discount = models.PositiveIntegerField(blank=True, null=True)
    information = RichTextUploadingField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    available = models.BooleanField(default=True)
    status = models.CharField(
        max_length=200, choices=STATUS_CHOICES, default='None', blank=True, null=True
    )
    image = models.ImageField(upload_to='product', blank=True, null=True)
    sell = models.IntegerField(default=0)
    total_favourite = models.IntegerField(default=0)
    change = models.BooleanField(default=True)
    num_view = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(Category, blank=True)
    color = models.ManyToManyField(Color, blank=True)
    favourite = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='fa_user', blank=True
    )
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='product_like', blank=True
    )
    unlike = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='product_unlike', blank=True
    )
    tags = TaggableManager(blank=True)
    size = models.ManyToManyField(Size, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount:
            return self.unit_price - (self.unit_price * self.discount // 100)
        return self.unit_price


class Images(models.Model):
    name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='image/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or str(self.id)


class Comment(models.Model):
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey(
        'self', related_name='comment_reply', blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.user} - {self.product}'


class Variants(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    amount = models.PositiveIntegerField(default=0)
    unit_price = models.PositiveBigIntegerField(default=0)
    discount = models.PositiveIntegerField(blank=True, null=True)
    change = models.BooleanField(default=True)
    color_variant = models.ForeignKey(
        Color, blank=True, null=True, on_delete=models.CASCADE
    )
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or str(self.id)

    @property
    def final_price(self):
        if self.discount:
            return self.unit_price - (self.unit_price * self.discount // 100)
        return self.unit_price


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.BigIntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(
        Product, related_name='pr_update', blank=True, null=True, on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        Variants, related_name='v_update', blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name or str(self.id)


class Views(models.Model):
    ip = models.CharField(max_length=200, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.product} - {self.create}'
