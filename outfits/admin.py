from django.contrib import admin

from outfits.models import Occasion, Outfit, OutfitGarment


# Register your models here.

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OutfitGarmentAdmin(admin.TabularInline):
    model = OutfitGarment
    extra = 1

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ('title', 'occasion', 'season', 'created_at')
    list_filter = ('occasion', 'season')
    search_fields = ('title',)
    ordering = ('-created_at',)
    inlines = [
        OutfitGarmentAdmin,
    ]


