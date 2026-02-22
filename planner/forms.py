"""
Forms for the planner application.

This module contains ModelForms and regular forms for managing plan entries,
including create, edit, and search functionality.
"""

from django import forms
from django.forms import ModelForm

from outfits.models import Outfit
from planner.models import PlanEntry


class PlanBaseForm(ModelForm):
    """
    Base form for creating and editing PlanEntry instances.

    Uses a radio select widget for outfit selection and a date picker
    for the plan date.
    """

    class Meta:
        model = PlanEntry
        fields = ["date", "outfit", "note"]
        labels = {
            "date": "Plan Date",
            "outfit": "Select Outfit",
            "note": "Additional Note",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "outfit": forms.RadioSelect,
            "note": forms.Textarea,
        }
        error_messages = {
            "date": {
                "unique": "A plan entry for this date already exists.",
                "required": "Please enter a date for the plan entry.",
            },
            "outfit": {
                "required": "Please select an outfit for the plan entry.",
            },
            "note": {
                "max_length": "Note cannot exceed 200 characters.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].required = True
        self.fields["outfit"].required = True
        self.fields["note"].required = False
        self.fields["note"].widget.attrs.update(
            {"placeholder": "Optional note (5-200 characters)", "rows": 4}
        )

        self.fields["outfit"].queryset = Outfit.objects.prefetch_related(
            "garments"
        ).order_by("-created_at")


class PlanCreateForm(PlanBaseForm):
    """Form for creating new PlanEntry instances."""

    pass


class PlanEditForm(PlanBaseForm):
    """Form for editing existing PlanEntry instances."""

    pass


class PlanSearchForm(forms.Form):
    """
    Search form for filtering plan entries by date and note content.

    All fields are optional to allow flexible filtering.
    """

    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Search by Date",
    )

    note = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Plan Note..."}),
        label="Search by Note",
    )
