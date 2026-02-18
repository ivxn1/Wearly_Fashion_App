"""
Forms for the wardrobe application.

This module contains ModelForms and regular forms for managing brands and garments,
including create, edit, and search functionality.
"""

from django import forms

from wardrobe.choices import GARMENT_CATEGORY_CHOICES
from core.choices import SeasonChoices

from wardrobe.models import Brand, Garment


class BrandBaseForm(forms.ModelForm):
    """
    Base form for creating and editing Brand instances.

    Provides validation for brand name and country fields,
    ensuring they contain only alphabetic characters.
    """

    class Meta:
        model = Brand
        fields = '__all__'
        labels = {
            'name': 'Brand Name',
            'country': 'Country of Origin',
            'website': 'Official Website',
        }
        widgets = {
            'name': forms.TextInput,
            'country': forms.TextInput,
            'website': forms.URLInput,
        }
        error_messages = {
            'name': {
                'required': "Please enter the brand name.",
                'length': "Brand name cannot exceed 80 characters.",
                'unique': "This brand name already exists.",
            },
            'country': {
                'length': "Country name cannot exceed 20 characters.",
            }
        }

    def clean(self):
        """
        Validate that name and country contain only alphabetic characters.

        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        country = cleaned_data.get('country')

        if name and not name.replace(" ", "").isalpha():
            self.add_error('name', "Brand name must contain only alphabetic characters and spaces.")

        if country:
            if not country.replace(" ", "").isalpha():
                self.add_error('country', "Country name must contain only alphabetic characters and spaces.")
            elif len(country) > 20:
                self.add_error('country', "Country name cannot exceed 20 characters.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['country'].required = False
        self.fields['website'].required = False
        self.fields['website'].widget.attrs.update({'placeholder': 'e.g. https://www.example.com'})

class BrandCreateForm(BrandBaseForm):
    """Form for creating new Brand instances."""
    pass


class BrandEditForm(BrandBaseForm):
    """Form for editing existing Brand instances."""
    pass


class BrandSearchForm(forms.Form):
    """
    Search form for filtering brands by name and country.

    All fields are optional to allow flexible filtering.
    """

    name = forms.CharField(
        required=False,
        label="Search by name",
    )

    country = forms.CharField(
        required=False,
        label="Country",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the blank "All Seasons" option remains for searching
        self.fields['name'].widget.attrs.update({'placeholder': 'Brand name...'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Brand country...'})



class GarmentBaseForm(forms.ModelForm):
    """
    Base form for creating and editing Garment instances.

    Provides comprehensive validation for garment fields including
    title, color, size, and material. The slug field is auto-generated
    and displayed as read-only.
    """

    class Meta:
        model = Garment
        fields = ['title', 'category', 'brand', 'color', 'size', 'material', 'slug', 'season', 'price', 'image']
        labels = {
            'title': 'Garment Title',
            'category': 'Category',
            'brand': 'Brand',
            'color': 'Color',
            'size': 'Size',
            'material': 'Material',
            'season': 'Season',
            'price': 'Price ($)',
            'image': 'Image',
            'slug': 'Slug (URL Identifier)',
        }
        widgets = {
            'title': forms.TextInput,
            'slug': forms.TextInput,
            'category': forms.Select,
            'brand': forms.Select,
            'color': forms.TextInput,
            'size': forms.TextInput,
            'material': forms.TextInput,
            'season': forms.Select,
            'price': forms.NumberInput,
            'image': forms.ClearableFileInput,
        }
        error_messages = {
            'title': {
                'required': "Please enter the garment title.",
            },
            'category': {
                'required': "Please select a category.",
            },
            'brand': {
                'required': "Please select a brand.",
            },
            'color': {
                'length': "Color cannot exceed 30 characters.",
            },
            'size': {
                'length': "Size cannot exceed 10 characters.",
            },
            'material': {
                'length': "Material cannot exceed 40 characters.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['brand'].required = True
        self.fields['color'].required = True
        self.fields['size'].required = False
        self.fields['material'].required = False
        self.fields['season'].required = True
        self.fields['price'].required = False
        self.fields['image'].required = False
        self.fields['slug'].disabled = True
        self.fields['slug'].widget.attrs['readonly'] = True

        # Remove the blank "All Seasons" and "All Categories" options in create/edit forms
        self.fields['season'].choices = [
            (value, label) for value, label in SeasonChoices.choices if value
        ]

        self.fields['category'].choices = [
            (value, label) for value, label in GARMENT_CATEGORY_CHOICES if value != "All"
        ]

        # Add placeholders for better UX
        self.fields['title'].widget.attrs.update({'placeholder': 'e.g., Classic Blue Jeans'})
        self.fields['color'].widget.attrs.update({'placeholder': 'e.g., Navy Blue'})
        self.fields['size'].widget.attrs.update({'placeholder': 'e.g., M, 32, L'})
        self.fields['material'].widget.attrs.update({'placeholder': 'e.g., Cotton, Denim, Wool'})
        self.fields['price'].widget.attrs.update({'placeholder': '0.00', 'step': '0.01', 'min': '0'})

    def clean(self):
        """
        Validate garment fields for proper character content.

        Returns:
            dict: The cleaned form data.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        color = cleaned_data.get('color')
        size = cleaned_data.get('size')
        material = cleaned_data.get('material')

        if title and not title.replace(" ", "").isalnum():
            self.add_error('title', "Title must contain only alphanumeric characters and spaces.")

        if color and not color.replace(" ", "").isalpha():
            self.add_error('color', "Color must contain only alphabetic characters and spaces.")

        if size and not size.replace(" ", "").isalnum():
            self.add_error('size', "Size must contain only alphanumeric characters and spaces.")

        if material and not material.replace(" ", "").isalpha():
            self.add_error('material', "Material must contain only alphabetic characters and spaces.")

        return cleaned_data

class GarmentCreateForm(GarmentBaseForm):
    """Form for creating new Garment instances."""
    pass


class GarmentEditForm(GarmentBaseForm):
    """Form for editing existing Garment instances."""
    pass


class GarmentSearchForm(forms.Form):
    """
    Search form for filtering garments by multiple criteria.

    Supports filtering by title, brand, category, season, and sorting options.
    All fields are optional to allow flexible filtering.
    """

    title = forms.CharField(
        required=False,
        label="Search by title",
    )

    brand = forms.ModelChoiceField(
        required=False,
        label="Brand",
        widget=forms.Select,
        empty_label="All Brands",
        queryset=Brand.objects.none()
    )

    category = forms.ChoiceField(
        required=False,
        label="Category",
        choices=GARMENT_CATEGORY_CHOICES,
        widget=forms.Select
    )

    season = forms.ChoiceField(
        required=False,
        label="Season",
        choices=SeasonChoices,
        widget=forms.Select
    )
    sort = forms.ChoiceField(
        required=False,
        label="Sort By",
        choices=[
            ('newest', 'Newest'),
            ('price_asc', 'Price: Low to High'),
            ('price_desc', 'Price: High to Low'),
        ],
        widget=forms.Select
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all()
        # Ensure the blank "All Seasons" option remains for searching
        self.fields['season'].choices = SeasonChoices.choices
        self.fields['title'].widget.attrs.update({'placeholder': 'Garment title...'})