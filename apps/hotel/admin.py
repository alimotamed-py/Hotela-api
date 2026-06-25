from django.contrib import admin
from .models import Hotel, HotelImage


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'city',
        'star',
        'owner',
        'is_active'
    ]

    list_filter = [
        'city',
        'star',
        'is_active'
    ]

    search_fields = [
        'name',
        'city'
    ]

    inlines = [
        HotelImageInline
    ]


admin.site.register(HotelImage)