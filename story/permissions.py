from rest_framework import permissions

SAFE_METHODS = ['GET']
SAFE_OBJECT_METHODS = ['GET', 'POST']


class StoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(view)
        is_owner = request.user == obj.author
        if request.method not in SAFE_OBJECT_METHODS:
            return is_owner

        return is_owner or not obj.is_draft
