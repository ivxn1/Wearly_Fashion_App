# TODO - CREATE FORM FOR OUTFITS

from django import forms

from outfits.models import Outfit


class OutfitBaseForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['title', 'occasion', 'season', 'notes', 'image', 'garments']
        labels = {
            'title': 'Title',
            'occasion': 'Occasion',
            'season': 'Season',
            'notes': 'Notes',
            'image': 'Image',
            'garments': 'Garments',
        }
        widgets = {
            'occasion': forms.Select,
            'season': forms.Select,
            'notes': forms.Textarea,
            'image': forms.ClearableFileInput,
            'garments': forms.ModelMultipleChoiceField,
        }
        error_messages = {
            'title': {
                'required': "Please enter the outfit name.",
                'length': "Brand name cannot exceed 120 characters.",
                'unique': "This brand name already exists.",
            },
            'occasion': {
                'length': "Country name cannot exceed 50 characters.",
                'required': "Please enter the country of origin.",
            },
            'season': {
                'required': "Please enter the outfit season.",
            },
            'garments': {
                'required': "Please select at least one garment for the outfit.",
            }
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
        self.fields['title'].required = True
        self.fields['occasion'].required = True
        self.fields['season'].required = True
        self.fields['notes'].required = False
        self.fields['image'].required = False
        self.fields['garments'].required = True
        self.fields['notes'].widget.attrs.update({'placeholder': 'Additional notes about the outfit...'})
        self.fields['title'].widget.attrs.update({'placeholder': 'e.g. Summer Casual'})
        self.fields['occasion'].widget.attrs.update({'placeholder': 'e.g. Beach Party'})
        self.fields['notes'].widget.attrs.update({'rows': 4, 'cols': 40}, {'placeholder': 'Additional notes about the outfit...'})

class OutfitCreateForm(OutfitBaseForm):
    pass

class OutfitEditForm(OutfitBaseForm):
    pass

