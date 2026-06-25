# ==================== ADD LIBRARY AND PACKAGE ====================
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from apps.account.models import CustomUser
from django.utils.translation import gettext_lazy as _


# ==================== ADDED USER FORM ====================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'role')
        
        
# ==================== EDIT USER FORM ====================
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        
        
# ==================== CUSTOM USER ADMIN ====================
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    ordering = ['phone_number']
    list_display = ['first_name', 'last_name', 'phone_number', 'email', 'role', 'created_at', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active', 'is_superuser']
    search_fields = ['phone_number', 'email']
    list_display_links = ['phone_number', 'email']
    
    fieldsets = (
        (_('اطلاعات ورود'), {'fields': ('phone_number', 'email', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name')}),
        (_('دسترسی‌ها'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخچه‌های مهم'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )