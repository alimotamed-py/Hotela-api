# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework.permissions import BasePermission


# ==================== OWNER OR ADMIN ====================
class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user.is_authenticated and
            getattr(request.user, "role", None) in [
                "owner",
                "admin"
            ]
        )

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "role", None) == "admin":
            return True

        return obj.owner == request.user