from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="first name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="middle name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="last name")
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    salary = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_accountant = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Accountant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empId = models.CharField(max_length=8, null=True, blank=True, unique=True)
    tin_number = models.CharField(max_length=9, null=True, blank=True)
    nssf_number = models.CharField(max_length=9, null=True, blank=True)
    isAccountant = models.BooleanField(default=True)
    salary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email

class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empId = models.CharField(max_length=8, null=True, blank=True, unique=True)
    tin_number = models.CharField(max_length=9, null=True, blank=True)
    nssf_number = models.CharField(max_length=9, null=True, blank=True)
    short_name = models.CharField(max_length=3, null=True, blank=True, unique=True)
    isTeacher = models.BooleanField(default=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class MessageToTeacher(models.Model):
    """ Stores a message to be shown to Teachers for a specific amount of time
    """
    message = models.TextField(help_text="This message will be shown to teachers when they log in.")
    start_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    def __str__(self):
        return self.message

