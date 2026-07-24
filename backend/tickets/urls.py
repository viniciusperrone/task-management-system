from rest_framework.routers import DefaultRouter
from tickets.views import BoardViewSet, ColumnViewSet, TicketViewSet


router = DefaultRouter()
router.register('board', BoardViewSet)
router.register('column', ColumnViewSet)
router.register('ticket', TicketViewSet)

urlpatterns = router.urls
