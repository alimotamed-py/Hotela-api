# ==================== ADD LIBRARY AND PACKAGE ====================
from django.urls import path
from apps.account import views
from rest_framework_simplejwt.views import TokenRefreshView



# ==================== URLS PATH ====================
app_name = 'account'

urlpatterns = [
    path('send-code/', views.SendCodeView.as_view(), name='send_code'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify-code'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
