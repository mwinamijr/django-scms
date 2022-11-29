from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
	 teacherProfileView, MyTokenObtainPairView, registerUser, getUserProfile, 
	 updateUserProfile, getUsers, getUserById, updateUser, deleteUser, UserListView
	 )

urlpatterns = [
    path('teacher-profile/<int:pk>/', teacherProfileView, name="teacher-profile"),
	path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', UserListView.as_view(), name='user-list'),
    path('profile/', getUserProfile, name="users-profile"),
    path('profile/update/', updateUserProfile, name="user-profile-update"),
    #path('', getUsers, name="users"),
    path('<str:pk>/', getUserById, name='user'),
    path('update/<str:pk>/', updateUser, name='user-update'),
    path('delete/<str:pk>/', deleteUser, name='user-delete'),
]


'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountantViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'accountants', AccountantViewSet)
router.register(r'teachers', TeacherViewSet)

urlpatterns = [
	path('', include(router.urls))
]
'''