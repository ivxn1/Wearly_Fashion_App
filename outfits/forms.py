from django import forms

from outfits.models import Outfit
from wardrobe.models import Garment


class OutfitBaseForm(forms.ModelForm):
    garments = forms.ModelMultipleChoiceField(
        queryset=Garment.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Select Garments'
    )

    class Meta:
        model = Outfit
        fields = ['title', 'occasion', 'season', 'notes', 'image', 'garments']
        labels = {
            'title': 'Outfit Title',
            'occasion': 'Occasion',
            'season': 'Season',
            'notes': 'Notes',
            'image': 'Outfit Image',
        }
        widgets = {
            'title': forms.TextInput,
            'occasion': forms.TextInput,
            'season': forms.Select,
            'notes': forms.Textarea,
            'image': forms.ClearableFileInput,
        }
        error_messages = {
            'title': {
                'required': "Please enter the outfit name.",
                'max_length': "Outfit title cannot exceed 120 characters.",
            },
            'occasion': {
                'max_length': "Occasion cannot exceed 50 characters.",
                'required': "Please enter the occasion.",
            },
            'season': {
                'required': "Please select the outfit season.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        occasion = cleaned_data.get('occasion')


        if title and not title.replace(" ", "").isalpha():
            self.add_error('title', "Outfit title must contain only alphabetic characters and spaces.")

        if occasion:
            if not occasion.replace(" ", "").isalpha():
                self.add_error('occasion', "Outfit occasion must contain only alphabetic characters and spaces.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Assign garments queryset
        self.fields['garments'].queryset = Garment.objects.select_related('brand').all()

        # Required/Not required fields
        self.fields['title'].required = True
        self.fields['occasion'].required = True
        self.fields['season'].required = True
        self.fields['notes'].required = False
        self.fields['image'].required = False
        self.fields['garments'].required = True

        # Placeholders
        self.fields['title'].widget.attrs.update({'placeholder': 'e.g., Summer Beach Party'})
        self.fields['occasion'].widget.attrs.update({'placeholder': 'e.g., Beach Party, Business Meeting'})
        self.fields['notes'].widget.attrs.update({'placeholder': 'Additional notes about this outfit...', 'rows': 4})

class OutfitCreateForm(OutfitBaseForm):
    pass

class OutfitEditForm(OutfitBaseForm):
    pass

