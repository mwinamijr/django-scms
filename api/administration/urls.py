from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ArticleViewSet, CarouselImageViewSet)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'carousel', CarouselImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
