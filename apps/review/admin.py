from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "hotel",
        "rating",
        "created_at"
    ]

    list_filter = [
        "rating"
    ]

    search_fields = [
        "user__phone_number",
        "hotel__name"
    ]