from django import forms
from django.forms import ModelForm
from outfits.models import Outfit
from planner.models import PlanEntry


class PlanBaseForm(ModelForm):
    class Meta:
        model = PlanEntry
        fields = ['date', 'outfit', 'note']
        labels = {
            'date': 'Plan Date',
            'outfit': 'Select Outfit',
            'note': 'Additional Note',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'outfit': forms.RadioSelect(),
            'note': forms.Textarea(attrs={'placeholder': 'Optional note (5-200 characters)', 'rows': 4}),
        }
        error_messages = {
            'date': {
                'unique': "A plan entry for this date already exists.",
                'required': "Please enter a date for the plan entry.",
            },
            'outfit': {
                'required': "Please select an outfit for the plan entry.",
            },
            'note': {
                'max_length': "Note cannot exceed 200 characters.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = True
        self.fields['outfit'].required = True
        self.fields['note'].required = False
        self.fields['note'].widget.attrs.update({'placeholder': 'Optional note (5-200 characters)'})
        self.fields['date'].widget.attrs.update({'type': 'date'})
        # Optimize outfit queryset with prefetching
        self.fields['outfit'].queryset = Outfit.objects.prefetch_related('garments').order_by('-created_at')

class PlanCreateForm(PlanBaseForm):
    pass

class PlanEditForm(PlanBaseForm):
    pass
