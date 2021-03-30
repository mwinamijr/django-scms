from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	ArticleViewSet, CarouselImageViewSet, PrimaryImageViewSet, 
	SecondaryImageViewSet, NurseryImageViewSet, DispensaryImageViewSet)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'carousel', CarouselImageViewSet)
router.register(r'primary', PrimaryImageViewSet)
router.register(r'secondary', SecondaryImageViewSet)
router.register(r'nursery', NurseryImageViewSet)
router.register(r'dispensary', DispensaryImageViewSet)

urlpatterns = [
	path('', include(router.urls))
]