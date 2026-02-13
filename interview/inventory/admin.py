from django.contrib import admin

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "language", "created_at", "updated_at")
    list_filter = ("type", "language", "tags")
    search_fields = ("name",)
    filter_horizontal = ("tags",)
    ordering = ("-created_at",)


@admin.register(InventoryLanguage)
class InventoryLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(InventoryTag)
class InventoryTagAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(InventoryType)
class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
