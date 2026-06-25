from rest_framework.permissions import BasePermission


class IsCustomerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user.is_authenticated and
            request.user.role in ["customer", "admin"]
        )


class IsReviewOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role == "admin":
            return True

        return obj.user == request.user