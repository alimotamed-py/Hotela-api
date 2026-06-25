from django.contrib import admin
from .models import Room, RoomImage, RoomAvailability


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class RoomAvailabilityInline(admin.TabularInline):
    model = RoomAvailability
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "hotel",
        "room_number",
        "room_type",
        "price_per_night",
        "capacity",
        "is_available"
    ]

    list_filter = [
        "room_type",
        "is_available"
    ]

    search_fields = [
        "room_number",
        "hotel__name"
    ]

    inlines = [
        RoomImageInline,
        RoomAvailabilityInline
    ]