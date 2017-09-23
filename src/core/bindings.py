# from django.core.paginator import Paginator
from channels_api.bindings import ResourceBinding
from channels_api.permissions import BasePermission
from .models import User
from .serializers import UserSerializer
# from django.conf import settings
from channels_api.decorators import list_action
from rest_framework.exceptions import NotFound


class Nobody(BasePermission):
    def has_permission(self, user, action, pk):
        if action == "info":
            return True
        return False


class UserBinding(ResourceBinding):
    model = User
    stream = "users"
    serializer_class = UserSerializer
    queryset = User.objects.filter()

    permission_classes = (Nobody,)

    @list_action()
    def info(self, data=None, **kwargs):
        if self.user is None:
            raise NotFound

        serializer = self.get_serializer(self.user)
        return serializer.data, 200
