from rest_framework.routers import DefaultRouter
from notes.views import AssignmentViewSet

router = DefaultRouter()
router.register(r'', AssignmentViewSet)
urlpatterns = router.urls
