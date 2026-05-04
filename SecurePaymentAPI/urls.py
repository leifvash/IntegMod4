from rest_framework.routers import DefaultRouter
from .views import PaymentRecordViewSet

router = DefaultRouter()
router.register(r'payment-records', PaymentRecordViewSet)

urlpatterns = router.urls