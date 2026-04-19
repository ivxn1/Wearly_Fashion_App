from django.contrib import admin

from planner.models import PlanEntry


@admin.register(PlanEntry)
class PlanEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "outfit", "created_at")
    list_filter = ("date",)
    search_fields = ("outfit__title",)
    ordering = ("-date",)
