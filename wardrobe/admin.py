from django.contrib import admin

from wardrobe.models import Brand, Garment

# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "brand",
        "category",
        "color",
        "season",
        "price",
        "created_at",
    )
    list_filter = ("brand", "category", "season")
    search_fields = ("title",)
    ordering = ("-created_at",)
