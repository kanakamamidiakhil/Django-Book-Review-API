from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAdminPasswordCorrect(BasePermission):
    def has_permission(self, request, view):
        admin_password = request.headers.get('admin-key')
        if admin_password != 'key123':
            raise PermissionDenied({"success": "false", "error": "Invalid admin password"})
        return True
