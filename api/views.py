from rest_framework import viewsets

from administration.models import Article, CarouselImage
from .serializers import (
	ArticleSerializer, CarouselImageSerializer)

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer

class CarouselImageViewSet(viewsets.ModelViewSet):
	queryset = CarouselImage.objects.all()
	serializer_class = CarouselImageSerializer

