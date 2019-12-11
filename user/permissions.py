from rest_framework import permissions

SAFE_METHODS = ['POST', 'GET']


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user.id == obj.id
        return True
