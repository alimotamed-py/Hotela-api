from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.shortcuts import redirect

def redirect_to_swagger(request):
    return redirect("swagger-ui")


urlpatterns = [
    path("", redirect_to_swagger),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.account.urls')),
    path('api/booking/', include('apps.booking.urls')),
    path('api/hotel/', include('apps.hotel.urls')),
    path('api/notification/', include('apps.notification.urls')),
    path('api/payment/', include('apps.payment.urls')),
    path('api/review/', include('apps.review.urls')),
    path('api/rooms/', include('apps.rooms.urls')),
]
