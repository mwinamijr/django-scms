from rest_framework import viewsets

from .models import Article, CarouselImage, PrimaryImage, SecondaryImage, NurseryImage, DispensaryImage
from .serializers import (
	ArticleSerializer, CarouselImageSerializer, PrimaryImageSerializer, 
	SecondaryImageSerializer, NurseryImageSerializer, DispensaryImageSerializer)

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer

class CarouselImageViewSet(viewsets.ModelViewSet):
	queryset = CarouselImage.objects.all()
	serializer_class = CarouselImageSerializer

class PrimaryImageViewSet(viewsets.ModelViewSet):
	queryset = PrimaryImage.objects.all()
	serializer_class = PrimaryImageSerializer

class SecondaryImageViewSet(viewsets.ModelViewSet):
	queryset = SecondaryImage.objects.all()
	serializer_class = SecondaryImageSerializer

class NurseryImageViewSet(viewsets.ModelViewSet):
	queryset = NurseryImage.objects.all()
	serializer_class = NurseryImageSerializer

class DispensaryImageViewSet(viewsets.ModelViewSet):
	queryset = DispensaryImage.objects.all()
	serializer_class = DispensaryImageSerializer
