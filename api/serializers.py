from rest_framework import serializers
from administration.models import Article, CarouselImage

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ['id', 'title', 'content', 'picture']

class CarouselImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = CarouselImage
		fields = ['id', 'title', 'description', 'picture']

