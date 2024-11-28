from rest_framework import permissions


class AdminORSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_seller is True:
            return user.is_staff or user.is_seller
        return False

