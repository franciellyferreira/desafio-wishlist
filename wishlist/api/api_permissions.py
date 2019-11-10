from rest_framework.permissions import BasePermission


class OnlyAdminCanCreate(BasePermission):
    def has_permission(self, request, view):
        if request == 'POST':
            return request.user.is_staff
        return True
