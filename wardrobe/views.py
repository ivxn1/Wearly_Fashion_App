"""
Views for the wardrobe application.

This module contains class-based views for managing garments and brands,
including list, detail, create, update, and delete operations.
"""

from django.db.models import Count, Avg
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, CreateView, DeleteView, UpdateView

from core.mixin import SetPaginateByMixin
from outfits.models import Outfit
from wardrobe.forms import GarmentSearchForm, GarmentCreateForm, BrandCreateForm, GarmentEditForm, BrandSearchForm
from wardrobe.models import Garment, Brand


# -------- GARMENT VIEWS --------- #

class GarmentListView(SetPaginateByMixin, ListView, FormView):
    """
    Display a paginated list of garments with search and filter functionality.

    Supports filtering by brand, category, season, and title search.
    Also supports sorting by price and creation date.
    """

    model = Garment
    template_name = 'wardrobe/garments/garments_list.html'
    context_object_name = 'wardrobe'
    paginate_by = 6
    form_class = GarmentSearchForm
    success_url = reverse_lazy('wardrobe:garment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or None
        return kwargs

    def get_queryset(self):
        qs = Garment.objects.select_related('brand').all()
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            brand_name = data.get('brand')
            if brand_name:
                qs = qs.filter(brand__name__icontains=brand_name)
            if data.get('category'):
                qs = qs.filter(category=data['category'])
            if data.get('season'):
                qs = qs.filter(season=data['season'])
            if data.get('title'):
                qs = qs.filter(title__icontains=data['title'])
            sort = data.get('sort', '').lower()
            if sort == 'price_asc':
                qs = qs.order_by('price')
            elif sort == 'price_desc':
                qs = qs.order_by('-price')
            elif sort == 'newest':
                qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, *args,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['page_title'] = 'Wearly Wardrobe'
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        return context

class GarmentDetailsView(DetailView):
    """
    Display detailed information about a single garment.

    Includes the outfits that contain this garment.
    """

    model = Garment
    template_name = 'wardrobe/garments/garment_details.html'
    context_object_name = 'garment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        garment = self.get_object()
        in_outfits = Outfit.objects.filter(outfitgarment__garment=garment).distinct()
        context['in_outfits'] = in_outfits
        context['page_title'] = f'Garment Details - {garment.title}'
        return context

class GarmentCreateView(CreateView):
    """Handle the creation of new garment entries."""

    template_name = 'wardrobe/garments/garment_add_form.html'
    form_class = GarmentCreateForm
    success_url = reverse_lazy('wardrobe:garment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Garment'
        return context


class GarmentDeleteView(DeleteView):
    """
    Handle garment deletion with protection for garments in outfits.

    Prevents deletion if the garment is part of any outfit.
    """

    model = Garment
    template_name = 'wardrobe/garments/garment_confirm_delete.html'
    success_url = reverse_lazy('wardrobe:garment_list')
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.outfitgarment_set.exists():
            messages.error(request, f'Cannot delete "{self.object.title}" because it is part of one or more outfits. Please remove it from all outfits before deleting.')
            return redirect('wardrobe:garment_details', slug=self.object.slug)
        return super().post(request, *args, **kwargs)

    extra_context = {
        'page_title': 'Wearly - Delete Garment',
    }


class GarmentEditView(UpdateView):
    """Handle updating existing garment information."""

    model = Garment
    form_class = GarmentEditForm
    template_name = 'wardrobe/garments/garment_edit_form.html'
    success_url = reverse_lazy('wardrobe:garment_list')

    extra_context = {
        'page_title': 'Wearly - Edit Garment',
    }


# --------- BRAND VIEWS --------- #

class BrandListView(SetPaginateByMixin, ListView, FormView):
    """
    Display a paginated list of brands with search functionality and statistics.

    Shows brand statistics including most used in outfits, most expensive,
    and brand with most garments.
    """

    model = Brand
    template_name = 'wardrobe/brands/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 6
    form_class = BrandSearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or None
        return kwargs

    def get_queryset(self):
        qs = Brand.objects.annotate(
            garment_count=Count('wardrobe')
        ).order_by('name').all()
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            if data.get('name'):
                qs = qs.filter(name__icontains=data['name'])
            if data.get('country'):
                qs = qs.filter(country__icontains=data['country'])
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Brands'
        context['most_used_in_outfits'] = Brand.objects.annotate(
            outfit_count=Count('wardrobe__outfitgarment__outfit', distinct=True)
        ).order_by('-outfit_count').first()
        context['most_expensive_brand'] = Brand.objects.annotate(
            avg_price=Avg('wardrobe__price')
        ).filter(avg_price__isnull=False).order_by('-avg_price').first()
        context['most_garments_brand'] = self.get_queryset().order_by('-garment_count').first()
        context['form'] = self.get_form()
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        return context

class BrandDetailsView(DetailView):
    """Display detailed information about a single brand including garment count."""

    template_name = 'wardrobe/brands/brand_details.html'
    context_object_name = 'brand'

    def get_queryset(self):
        return Brand.objects.annotate(
            garment_count=Count('wardrobe')
        ).all()


    extra_context = {
        'page_title': 'Brand Details',
    }


class BrandCreateView(CreateView):
    """Handle the creation of new brand entries."""

    model = Brand
    form_class = BrandCreateForm
    template_name = 'wardrobe/brands/brand_add_form.html'
    success_url = reverse_lazy('wardrobe:brand_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Brand'
        return context


class BrandEditView(UpdateView):
    """Handle updating existing brand information."""

    model = Brand
    form_class = BrandCreateForm
    template_name = 'wardrobe/brands/brand_edit_form.html'
    context_object_name = 'brand'

    def get_success_url(self):
        return reverse_lazy('wardrobe:brand_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit Brand - {self.object.name}'
        return context


class BrandDeleteView(DeleteView):
    """
    Handle brand deletion with protection for brands with garments.

    Prevents deletion if the brand has any associated garments.
    """

    model = Brand
    template_name = 'wardrobe/brands/brand_confirm_delete.html'
    context_object_name = 'brand'
    success_url = reverse_lazy('wardrobe:brand_list')

    def get_queryset(self):
        return Brand.objects.annotate(garment_count=Count('wardrobe'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.garment_count > 0:
            messages.error(
                request,
                f'Cannot delete "{self.object.name}" because it has {self.object.garment_count} garment(s) connected to it. '
                f'Please remove or reassign all garments before deleting this brand.'
            )
            return redirect('wardrobe:brand_details', pk=self.object.pk)
        messages.success(request, f'Brand "{self.object.name}" has been successfully deleted.')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete Brand - {self.object.name}'
        return context
