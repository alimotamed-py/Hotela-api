# ==================== ADD LIBRARY AND PACKAGE ====================
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils.translation import gettext_lazy as _
from apps.account.serializers import *




# ==================== SEND CODE VIEW ====================
class SendCodeView(APIView):
    """
    Send a verification code to a user's phone number.\n
    POST /api/account/send-code/\n
    Permissions: AllowAny
    """

    permission_classes = [permissions.AllowAny]
    
    @extend_schema(tags=['Send Code'])
    def post(self, request):
        serializer = SendCodeSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : _('کد تایید ارسال شد.')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# ==================== VERIFY CODE VIEW ====================
class VerifyCodeView(APIView):
    """
    Verify phone code and issue JWT tokens. \n
    POST /api/account/verify-code/ \n
    Permissions: AllowAny
    """
    
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(tags=['Verify Code'])
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            token =serializer.save()
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# ==================== USER PROFILE VIEW ====================
class ProfileView(APIView):
    """
    Retrieve or update authenticated user's profile.\n
    GET / PATCH /api/account/profile/\n
    Permissions: IsAuthenticated
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(tags=['Profile User'])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(tags=['Update Profile User'])
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
# ==================== USER LOGOUT VIEW ====================      
class UserLogoutView(APIView):
    """
    Log out authenticated user and blacklist refresh token.
    POST /api/account/logout/
    Permissions: IsAuthenticated
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializers = UserLogoutSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message' : _('با موفقیت خارج شدید.')}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)