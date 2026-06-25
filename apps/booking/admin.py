# ==================== ADD LIBRARY AND PACKAGE ====================
from django.contrib import admin
from .models import Booking

# ==================== ADMIN REGISTER ====================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = ["id", "customer", "room", "check_in", "check_out", "status", "total_price"]

    list_filter = ["status"]

    search_fields = ["customer__phone_number", "room__room_number"]