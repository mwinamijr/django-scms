from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountantViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'accountants', AccountantViewSet)
router.register(r'teachers', TeacherViewSet)

urlpatterns = [
	path('', include(router.urls))
]