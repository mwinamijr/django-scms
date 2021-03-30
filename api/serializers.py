from rest_framework import serializers
from .models import Article, CarouselImage, PrimaryImage, SecondaryImage, NurseryImage, DispensaryImage

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ['id', 'title', 'content', 'picture']

class CarouselImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = CarouselImage
		fields = ['id', 'title', 'description', 'picture']

class PrimaryImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = PrimaryImage
		fields = ['id', 'title', 'description', 'picture']

class SecondaryImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = SecondaryImage
		fields = ['id', 'title', 'description', 'picture']

class NurseryImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = NurseryImage
		fields = ['id', 'title', 'description', 'picture']

class DispensaryImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = DispensaryImage
		fields = ['id', 'title', 'description', 'picture']
