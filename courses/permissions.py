
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Check if user has is_superuser flag set to give admin permissions
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser