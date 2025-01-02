from rest_framework.permissions import BasePermission


class PostOwnerOnly(BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if authenticated user is the owner
        return obj.user == request.user
