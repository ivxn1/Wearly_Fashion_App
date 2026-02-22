"""
Views for the outfits application.

This module contains class-based views for managing outfits,
including list, detail, create, update, and delete operations.
"""

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from core.mixin import SetPaginateByMixin
from outfits.forms import OutfitCreateForm, OutfitSearchForm
from outfits.models import Outfit


class OutfitsListView(SetPaginateByMixin, ListView, FormView):
    """
    Display a paginated list of outfits with search and filter functionality.

    Supports filtering by title, occasion, and season.
    """

    model = Outfit
    template_name = "outfits/outfits_list.html"
    context_object_name = "outfits"
    paginate_by = 6
    form_class = OutfitSearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.GET or None
        return kwargs

    def get_queryset(self):
        qs = Outfit.objects.prefetch_related("garments")
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            if data.get("title"):
                qs = qs.filter(title__icontains=data["title"])
            if data.get("occasion"):
                qs = qs.filter(occasion__icontains=data["occasion"])
            if data.get("season"):
                qs = qs.filter(season=data["season"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Wearly Outfits"
        context["form"] = self.get_form()
        context["paginate_by"] = self.get_paginate_by(self.get_queryset())
        return context


class OutfitDetailsView(DetailView):
    """
    Display detailed information about a single outfit.

    Shows all garments included in the outfit.
    """

    model = Outfit
    template_name = "outfits/outfit_details.html"
    context_object_name = "outfit"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.object.title
        context["outfit_garments"] = self.object.garments.all()
        return context


class AddOutfitView(CreateView):
    """Handle the creation of new outfit entries with garment selection."""

    model = Outfit
    form_class = OutfitCreateForm
    template_name = "outfits/outfit_add_form.html"

    def get_success_url(self):
        return reverse_lazy("outfits:outfit_details", kwargs={"id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Outfit"
        return context


class EditOutfitView(UpdateView):
    """Handle updating existing outfit information and garment selection."""

    model = Outfit
    form_class = OutfitCreateForm
    template_name = "outfits/outfit_edit_form.html"
    context_object_name = "outfit"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse_lazy("outfits:outfit_details", kwargs={"id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit {self.object.title}"
        return context


class DeleteOutfitView(DeleteView):
    """Handle outfit deletion with confirmation."""

    model = Outfit
    template_name = "outfits/outfit_confirm_delete.html"
    context_object_name = "outfit"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("outfits:outfits_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete {self.object.title}"
        return context
