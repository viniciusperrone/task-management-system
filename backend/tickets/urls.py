from rest_framework.routers import DefaultRouter
from tickets.views import BoardViewSet, ColumnViewSet, TicketViewSet


router = DefaultRouter()
router.register('/board', BoardViewSet, basename='board')
router.register('/column', ColumnViewSet, basename='column')
router.register('/ticket', TicketViewSet, basename='ticket')

urlpatterns = router.urls
