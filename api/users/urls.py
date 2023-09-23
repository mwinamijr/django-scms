from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
	 MyTokenObtainPairView, UserListView, UserDetailView,
	 AccountantListView, AccountantDetailView
	 )
from academic.views import TeacherListView, TeacherDetailView
urlpatterns = [
	path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', UserListView.as_view(), name='user-list'),
    
    path('accountants/', AccountantListView.as_view(), name='accountant-list'),
    path('accountants/<str:pk>/', AccountantDetailView.as_view(), name='accountant-details'),
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<str:pk>/', TeacherDetailView.as_view(), name='teacher-details'),
    path('<str:pk>/', UserDetailView.as_view(), name='user-details'),
]
