from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from .managers import CustomUserManager
from administration.common_objs import *
from academic.models import Subject


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="first name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="middle name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="last name")
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
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
    inactive = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=250, blank=True)
    first_name = models.CharField(max_length=300, verbose_name="First Name", blank=True)
    last_name = models.CharField(max_length=300, verbose_name="Last Name", blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=True)
    email = models.EmailField(blank=True, null=True)
    teacher_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    empId = models.CharField(max_length=8, null=True, blank=True, unique=True)
    middle_name = models.CharField(max_length=100, blank=True)
    tin_number = models.CharField(max_length=9, null=True, blank=True)
    nssf_number = models.CharField(max_length=9, null=True, blank=True)
    short_name = models.CharField(max_length=3, null=True, blank=True, unique=True)
    isTeacher = models.BooleanField(default=True)
    salary = models.IntegerField(blank=True, null=True)
    subject_specialization = models.ManyToManyField(Subject, blank=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    alt_email = models.EmailField(blank=True, null=True, help_text="Personal Email apart from the one given by the school")
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='Teacher_images', blank=True, null=True)

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def deleted(self):
        # for backward compatibility
        return self.inactive

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        #  check if the person is already a student
        #if Student.objects.filter(id=self.id).count():
        #    raise ValidationError("cannot have a someone be a student and a Teacher")

        # save model
        super(Teacher, self).save()

        # create a user with default password as firstname and lastname
        user, created = CustomUser.objects.get_or_create(email=self.email, first_name=self.first_name, last_name=self.last_name, is_teacher=self.is_teacher)
        if created:
            user.password = (str(self.first_name) + str(self.last_name))
            user.save()
            # send the username and password to email
            msg = "\nHey {} Welcome to {}, your username is {} and the default one time password is {}" \
                  "Please login to your portal and change the password.." \
                  "This password is valid for 24 hours only".format((str(self.first_name) + str(self.last_name)), "this school ",self.username, user.password
                                                                    )
            #mail_agent(self.alt_email, "Default user Name and password", msg)

        # add the user to a Group
        group, gcreated = Group.objects.get_or_create(name='teacher')
        if gcreated:
            group.save()
        user.groups.add(group)
        user.save()


class MessageToTeacher(models.Model):
    """ Stores a message to be shown to Teachers for a specific amount of time
    """
    message = models.TextField(help_text="This message will be shown to teachers when they log in.")
    start_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(auto_now_add=False, validators=settings.DATE_VALIDATORS)
    def __str__(self):
        return self.message

