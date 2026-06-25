# ==================== ADD LIBRARY ====================
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .pagination import NotificationPagination


# ==================== READ NOTIFICATION ====================
class NotificationReadView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            user=request.user
        )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {
                "message": "اعلان خوانده شد"
            },
            status=status.HTTP_200_OK
        )


# ==================== LIST NOTIFICATIONS ====================
class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = NotificationPagination

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).only(
            "id",
            "title",
            "message",
            "type",
            "is_read",
            "created_at"
        )