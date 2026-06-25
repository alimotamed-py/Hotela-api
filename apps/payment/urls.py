from django.urls import path
from .views import PaymentCreateView, PaymentVerifyView

urlpatterns = [
    path("create/", PaymentCreateView.as_view()),
    path("verify/", PaymentVerifyView.as_view()),
]