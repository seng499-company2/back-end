from rest_framework import permissions;


class IsAdmin(permissions.BasePermission):
    """
    Check if user has is_superadmin flag set to give admin permissions
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user.id == request.user.id