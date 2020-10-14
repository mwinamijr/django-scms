from django.db import models

class Article(models.Model):
	title = models.CharField(max_length=150, blank=True, null=True)
	content = models.TextField()
	#picture = models.ImageField()

	def __str__(self):
		return self.title