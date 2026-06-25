# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework.permissions import BasePermission


# ==================== CUSTOMER PERMISSION ====================
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'customer') 
    
    
 
 # ==================== OWNER PERMISSION ====================   
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'owner')
    
    
 
# ==================== ADMIN PERMISSION ====================   
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
         return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')
            


# ==================== HOTEL OWNER PERMISSION ====================    
class IsHotelOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    (request.user.role == 'admin' or request.user.role == 'owner'))
        
        
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        return obj.owner == request.user
