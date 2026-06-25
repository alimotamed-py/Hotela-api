# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework.permissions import BasePermission

# ==================== CUSTOMER OR ADMIN ====================
class IsCustomerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return bool(request.user.is_authenticated and
                    getattr(request.user, "role", None) in ["customer", "admin"])

# ==================== OWNER OR ADMIN ====================
class IsBookingOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if getattr(request.user, "role", None) == "admin":
            return True

        return obj.customer == request.user