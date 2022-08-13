from rest_framework_nested import routers
# ============================================================================ #
from . import views


# ================================== ROUTERS ================================= #

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewSet)

urlpatterns = router.urls
