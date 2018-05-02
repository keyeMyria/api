from channels_api.permissions import BasePermission


class AllowCreate(BasePermission):
    def has_permission(self, user, action, pk):
        return action == 'create'
