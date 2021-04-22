from django.db import models
import httpagentparser
from users.models import CustomUser

from datetime import datetime

class Article(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="articles", blank=True, null=True)

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
    ua = models.CharField(max_length=2000, help_text="User agent. We can use this to determine operating system and browser in use.")
    date = models.DateTimeField(default=datetime.now)
    ip = models.GenericIPAddressField()
    usage = models.CharField(max_length=255)
    def __str__(self):
        return str(self.login) + " " + str(self.usage) + " " + str(self.date)
    def os(self):
        try:
            return httpagentparser.simple_detect(self.ua)[0]
        except:
            return "Unknown"
    def browser(self):
        try:
            return httpagentparser.simple_detect(self.ua)[1]
        except:
            return "Unknown"