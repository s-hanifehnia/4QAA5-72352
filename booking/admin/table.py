from django.contrib import admin

from booking.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name", "seats")
    search_fields = ("name", "seats")
