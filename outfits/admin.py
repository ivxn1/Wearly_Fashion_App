from django.contrib import admin

from outfits.models import Outfit, OutfitGarment


class OutfitGarmentAdmin(admin.TabularInline):
    model = OutfitGarment
    extra = 1


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("title", "occasion", "season", "created_at")
    list_filter = ("occasion", "season")
    search_fields = ("title",)
    ordering = ("-created_at",)
    inlines = [
        OutfitGarmentAdmin,
    ]
