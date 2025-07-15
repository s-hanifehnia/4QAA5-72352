from django.contrib import admin
from booking.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "table",
        "requested_seats",
        "reserved_seats",
        "cost",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at", "table")
    search_fields = ("user__username", "table__name")
    ordering = ("-created_at",)
