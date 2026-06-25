# ==================== ADD LIBRARY AND PACKAGE ====================
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import timedelta





# ==================== BASE USER MANAGE ====================
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('شماره موبایل الزامی است'))
        if email:
            email = self.normalize_email(email)
            
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # ===================== SUPERUSER ====================
    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if password is None:
            raise ValueError(_('Superuser must have a password.'))
        
        
        return self.create_user(phone_number, email, password, **extra_fields)


# ==================== USER MODEL ====================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    class UserRole(models.TextChoices):
        ADMIN = 'admin', _('ادمین')
        CUSTOMER = 'customer', _('مشتری')
        OWNER = 'owner', _('صاحب هتل')
        
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('نام خانوادگی'))
    role = models.CharField(max_length=8, choices=UserRole.choices, default=UserRole.CUSTOMER, 
                            verbose_name=_('نقش کاربر'))
    
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('شماره موبایل'))
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_('ایمیل'))
    
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    is_staff = models.BooleanField(default=False, verbose_name=_('عضو پنل ادمین'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number} - ({self.get_role_display()})'

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


# ==================== PHONE OTP MODEL ====================
class PhoneOtp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps', blank=True, null=True)
    phone_number = models.CharField(max_length=11, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_used = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.phone_number} - {self.code}"
    
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=2)
    
    
    class Meta:
        verbose_name = _('کد تأیید')
        verbose_name_plural = _('کدهای تأیید')
        
        

        