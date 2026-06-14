from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phone_field.models import PhoneField


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(_('Username'), max_length=50)
    email = models.EmailField(_('Email'), unique=True)
    phone = PhoneField(_('Phone'), blank=True, null=True)
    f_name = models.CharField(_('First name'), max_length=100, blank=True, default='')
    l_name = models.CharField(_('Last name'), max_length=100, blank=True, default='')
    address = models.CharField(_('Address'), max_length=300, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile', blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_user_permissions(self, obj=None):
        return self.get_all_permissions(obj)

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        if not self.is_active or not self.is_admin:
            return set()
        from django.contrib.auth.models import Permission
        return {
            f'{perm.content_type.app_label}.{perm.codename}'
            for perm in Permission.objects.all()
        }


class EmailToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.email} - {self.token[:20]}'
