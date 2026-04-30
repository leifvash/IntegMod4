from rest_framework.routers import DefaultRouter
from .views import StudentRecordViewSet

router = DefaultRouter()
router.register(r'student-records', StudentRecordViewSet)

urlpatterns = router.urls