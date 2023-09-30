from django.db import models
import httpagentparser
from django.conf import settings
from datetime import date, datetime

from .common_objs import *
from users.models import CustomUser


class Article(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="articles", blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CarouselImage(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="carousel")

    def __str__(self):
        return self.title


class AccessLog(models.Model):
    login = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    ua = models.CharField(
        max_length=2000,
        help_text="User agent. We can use this to determine operating system and browser in use.",
    )
    date = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    usage = models.CharField(max_length=255)

    def __str__(self):
        return str(self.login) + " " + str(self.usage) + " " + str(self.date)

    def os(self):
        try:
            return httpagentparser.simple_detect(self.ua)[0]
            # return "what?"
        except:
            return "Unknown"

    def browser(self):
        try:
            return httpagentparser.simple_detect(self.ua)[1]
            # return "what?"
        except:
            return "Unknown"


class School(models.Model):
    active = models.BooleanField(
        default=False,
        help_text="DANGER..!!!! If marked this will be the default School Information System Wide...",
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    school_type = models.CharField(
        max_length=25, choices=SCHOOL_TYPE_CHOICE, blank=True, null=True
    )
    students_gender = models.CharField(
        max_length=25, choices=SCHOOL_STUDENTS_GENDER, blank=True, null=True
    )
    ownership = models.CharField(
        max_length=25, choices=SCHOOL_OWNERSHIP, blank=True, null=True
    )
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True)
    school_email = models.EmailField(blank=True, null=True)
    school_logo = models.ImageField(blank=True, null=True, upload_to="school_info")

    def __str__(self):
        return self.name


class Day(models.Model):
    dayOfWeek = (
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursday"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("7", "Sunday"),
    )
    day = models.CharField(max_length=1, choices=dayOfWeek, unique=True)

    def __str__(self):
        return self.day

    class Meta:
        ordering = ("day",)


class AcademicYear(models.Model):
    """
    a db table row that maps on every academic year
    """

    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    graduation_date = models.DateField(
        blank=True, null=True, help_text="The date when students graduate"
    )
    # week_days = models.ManyToManyField(Day)
    active_year = models.BooleanField(
        help_text="DANGER!! This is the current school year. There can only be one and setting this will remove it from other years. "
        "If you want to change the active year you almost certainly want to click Admin, Change School Year."
    )

    class Meta:
        ordering = ("-start_date",)

    def __str__(self):
        return self.name

    @property
    def status(self, now_=date.today()):
        if self.active_year:
            return "active"
        elif self.start_date <= now_ >= self.end_date:
            return "ended"

        elif self.start_date > now_ < self.end_date:
            return "pending"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(AcademicYear, self).save()
        if self.active_year:
            # if it is marked as the current year the update all the tables row i the database with false
            AcademicYear.objects.exclude(pk=self.pk).update(active_year="False")
