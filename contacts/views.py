from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Contact, Group
from .permissions import IsContactOwner
from .serializers import GroupSerializer, ContactSerializer


class GroupViewSet(ReadOnlyModelViewSet):
    """
        This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = IsAuthenticated,


class ContactViewSet(ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """

    def get_queryset(self):
        return Contact.objects.all()

    def get_serializer_class(self):
        return ContactSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = IsAuthenticated,
        elif self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = IsAuthenticated, IsContactOwner
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]
