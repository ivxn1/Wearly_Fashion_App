from django import forms

from core.mixins import DeleteFormMixin
from wardrobe.choices import GARMENT_CATEGORY_CHOICES, SeasonChoices
from wardrobe.models import Brand, Garment


class BrandBaseForm(forms.ModelForm):
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
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        website = cleaned_data.get('website')
        country = cleaned_data.get('country')

        if name and not name.replace(" ", "").isalpha():
            self.add_error('name', "Brand name must contain only alphabetic characters and spaces.")

        if country:
            if country.replace(" ", "").isalpha():
                self.add_error('country', "Country name must contain only alphabetic characters and spaces.")
            elif len(country) > 20:
                self.add_error('country', "Country name cannot exceed 20 characters.")

        if website:
            if not (website.startswith("http://") or website.startswith("https://")):
                self.add_error('website', "Website URL must start with 'http://' or 'https://'.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['country'].required = False
        self.fields['website'].required = False
        self.fields['website'].widget.attrs.update({'placeholder': 'e.g. https://www.example.com'})

class BrandCreateForm(BrandBaseForm):
    pass

class BrandEditForm(BrandBaseForm):
    pass

class BrandDeleteForm(DeleteFormMixin, BrandBaseForm):
    pass


class GarmentBaseForm(forms.ModelForm):
    class Meta:
        model = Garment
        fields = ['title', 'category', 'brand', 'color', 'size', 'material', 'season', 'price', 'image']
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
        }
        widgets = {
            'title': forms.TextInput,
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

    def clean(self):
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
    pass

class GarmentEditForm(GarmentBaseForm):
    pass

class GarmentDeleteForm(DeleteFormMixin, GarmentBaseForm):
    pass


class GarmentSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label="Search",
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
        self.fields['title'].widget.attrs.update({'placeholder': 'Search by title...'})