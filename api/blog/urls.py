from django.urls import path, include
from api.views import (
        ArticleListView, ArticleDetailView
)

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name="articles-list"),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name="article-detail"),
]
