from rest_framework.routers import DefaultRouter

from contacts.views import ContactViewSet, GroupViewSet

router = DefaultRouter()

router.register(
    r'ContactService',
    ContactViewSet,
    basename='ContactService')

router.register(
    r'GroupService',
    GroupViewSet,
    basename='GroupService')

urlpatterns = router.urls
