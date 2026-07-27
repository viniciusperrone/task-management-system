from rest_framework.routers import DefaultRouter
from tickets.views import BoardViewSet, ColumnViewSet, TicketViewSet, MessageViewSet


app_name = "tickets"

router = DefaultRouter()
router.register('/board', BoardViewSet, basename='board')
router.register('/column', ColumnViewSet, basename='column')
router.register('/ticket', TicketViewSet, basename='ticket')
router.register('/message', MessageViewSet, basename='message')

urlpatterns = router.urls
