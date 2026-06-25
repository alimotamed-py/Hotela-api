# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.translation import gettext_lazy as _
from apps.account.models import CustomUser, PhoneOtp
from django.utils import timezone
from datetime import timedelta
import secrets  
import string 
import logging
import re



logger = logging.getLogger(__name__)


# ==================== USER SERIALIZER ===================
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving or updating user information.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'email', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('id', 'phone_number', 'role', 'created_at')
        

        
# ==================== PHONE VALIDATION ===================
IRAN_PHONE = re.compile(r'^09\d{9}$')

def validate_iran_phone(value):
    value = value.strip()
    if not IRAN_PHONE.match(value):
        raise serializers.ValidationError(_('شماره موبایل معتبر نیست. فرمت درست مثل 09123456789'))
    return value



# ==================== SEND CODE SERIALIZER ===================
class SendCodeSerializer(serializers.Serializer):
    """
    Serializer for sending verification code to a user's phone number.
    """

    phone_number = serializers.CharField(max_length=11)
    
    RATE_LIMIT_WINDOW = timedelta(minutes=1)           # Minimum distance between two codes for a phone number
    MAX_PER_WINDOW = 1                                 # Maximum number in this range
    MAX_PER_HOUR = 5                                   # Maximum number in one hour
    
    def validate_phone_number(self, value):
        return validate_iran_phone(value)
    
    def validate(self, attrs):
        phone = attrs['phone_number']
        
        now = timezone.now()
        one_minute_ago = now - self.RATE_LIMIT_WINDOW
        one_hour_ago = now - timedelta(hours=1)
    
        # Number of codes sent in the last minute
        count_last_minute = PhoneOtp.objects.filter(phone_number=phone, created_at__gte=one_minute_ago).count()
        
        if count_last_minute >= self.MAX_PER_WINDOW:
            raise serializers.ValidationError({'phone_number': _('کد قبلاً ارسال شده، لطفاً یک دقیقه بعد دوباره تلاش کنید')})
        
        # Number of codes sent in the last hour
        count_last_hour = PhoneOtp.objects.filter(phone_number=phone, created_at__gte=one_hour_ago).count()
        
        if count_last_hour >= self.MAX_PER_HOUR:
            raise serializers.ValidationError(
                 {'phone_number': _('تعداد درخواست کد برای این شماره بیش از حد مجاز است، بعداً تلاش کنید')}
            )
            
        return attrs
    
    
    def create(self, validated_data):
        phone = validated_data['phone_number']
        user, created = CustomUser.objects.get_or_create(phone_number=phone, defaults={'email' : None})
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        otp =PhoneOtp.objects.create(phone_number=phone, user=user, code=code)
        
        #=============================================================
        logger.info(f"OTP generated for {phone}. Code: {code}")
        # SMS PANEL API
        #=============================================================
        return otp
    

  
# ==================== VERIFY CODE SERIALIZER ====================
class VerifyCodeSerializer(serializers.Serializer):
    """
    Serializer for verifying the code sent to user's phone number
    and issuing JWT tokens.
    """
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
    
    def validate_phone_number(self, value):
        return validate_iran_phone(value)
    
    def validate_code(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError(_('کد باید فقط عدد باشد'))
        if len(value) != 6:
            raise serializers.ValidationError(_('طول کد نامعتبر است'))
        return value
    
    
    def validate(self, attrs):
        phone = attrs.get('phone_number')
        code = attrs.get('code')
        
        try:
            otp =PhoneOtp.objects.filter(phone_number=phone, code=code, is_used=False).latest('created_at')
        except PhoneOtp.DoesNotExist:
            raise serializers.ValidationError({'code': _('کد نامعتبر است')})
        
        if otp.is_expired():
            raise serializers.ValidationError({'code': _('کد منقضی شده است')})
        
        attrs['user'] = otp.user
        attrs['otp'] = otp
        
        return attrs
    

    
    def create(self, validated_data):
        user = validated_data['user']
        otp = validated_data['otp']
        
        otp.is_used = True
        otp.save()
        
        
        refresh =RefreshToken.for_user(user)
        return {
            'message': _('به هتلا خوش آمدید'),
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        
        
# ==================== USER LOGOUT ====================
class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for logging out a user by blacklisting their refresh token.
    """
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs.get('refresh')
        if not self.token:
            raise serializers.ValidationError({'refresh': _('رفرش توکن الزامی است.')})
        return attrs
    
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError({'refresh': _('توکن نامعتبر است یا قبلاً باطل شده.')})
            