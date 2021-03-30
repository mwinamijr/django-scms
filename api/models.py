from django.db import models

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

class NurseryImage(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="nursery")

	def __str__(self):
		return self.title

class PrimaryImage(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="primary")

	def __str__(self):
		return self.title

class SecondaryImage(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="secondary")

	def __str__(self):
		return self.title

class DispensaryImage(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	picture = models.ImageField(upload_to="dispensary")

	def __str__(self):
		return self.title