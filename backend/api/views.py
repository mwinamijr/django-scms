from rest_framework import viewsets, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import Http404

from administration.models import Article, CarouselImage
from .serializers import (
	ArticleSerializer, CarouselImageSerializer)

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer

class CarouselImageViewSet(viewsets.ModelViewSet):
	queryset = CarouselImage.objects.all()
	serializer_class = CarouselImageSerializer


class ArticleListView(views.APIView):
	"""
    List all articles, or create a new article.
    """
	def get(self, request, format=None):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ArticleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(views.APIView):
	def get_object(self, pk):
		try:
			return Article.objects.get(pk=pk)
		except Article.DoesNotExist:
			raise Http404
	def get(self, request, pk, format=None):
		article = self.get_object(pk)
		serializer = ArticleSerializer(article)
		return Response(serializer.data)
		
	def put(self, request, pk, format=None):
		article = self.get_object(pk)
		serializer = ArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		article = self.get_object(pk)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

