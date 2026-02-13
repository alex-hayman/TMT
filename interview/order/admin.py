from django.contrib import admin

from interview.order.models import Order, OrderTag


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("inventory", "start_date", "embargo_date", "is_active", "created_at")
    list_filter = ("is_active", "tags", "start_date", "embargo_date")
    search_fields = ("inventory__name",)
    filter_horizontal = ("tags",)
    ordering = ("-created_at",)
    date_hierarchy = "start_date"


@admin.register(OrderTag)
class OrderTagAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
