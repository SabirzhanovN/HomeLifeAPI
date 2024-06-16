from rest_framework.permissions import BasePermission


class IsAdminUserOrCreateOnly(BasePermission):
    """
    Custom permission to only allow admin users to delete/listing an object.
    """

    def has_permission(self, request, view):
        # Allow any authenticated user to create an order (POST request)
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        # Allow only admin users to delete an order (DELETE request)
        if request.method == 'DELETE' or request.method == 'GET':
            return request.user and request.user.is_staff

        return False
