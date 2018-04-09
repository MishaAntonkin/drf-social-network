from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser


class AdminCreate(BasePermission):

    def has_permission(self, request, view):
        print(request.user.is_superuser)
        print("In has permission")
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        else:
            return False
