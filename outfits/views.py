"""
Views for the outfits application.

This module contains class-based views for managing outfits,
including list, detail, create, update, and delete operations.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from django.views.generic.base import View

from accounts.models import FavouriteOutfits, Wishlist
from core.mixin import IsUserOwnerMixin, SetPaginateByMixin
from outfits.forms import (
    OutfitCreateForm,
    OutfitSearchForm,
    StyleBoardCreateForm,
    StyleBoardEditForm,
)
from outfits.models import Outfit, StyleBoard


class OutfitsListView(LoginRequiredMixin, SetPaginateByMixin, ListView, FormView):
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
        qs = super().get_queryset()
        qs = qs.prefetch_related("garments")
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
        favourites, _ = FavouriteOutfits.objects.get_or_create(user=self.request.user)
        context["favourites_ids"] = set(favourites.outfits.values_list("id", flat=True))
        return context


class OutfitDetailsView(LoginRequiredMixin, DetailView):
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
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        context["wishlist_ids"] = set(wishlist.garments.values_list("id", flat=True))
        return context


class AddOutfitView(LoginRequiredMixin, CreateView):
    """Handle the creation of new outfit entries with garment selection."""

    model = Outfit
    form_class = OutfitCreateForm
    template_name = "outfits/outfit_add_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("outfits:outfit_details", kwargs={"id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Outfit"
        return context


class EditOutfitView(IsUserOwnerMixin, LoginRequiredMixin, UpdateView):
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


class DeleteOutfitView(IsUserOwnerMixin, LoginRequiredMixin, DeleteView):
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


class FavouriteOutfitView(LoginRequiredMixin, View):
    def post(self, request, id):
        outfit = get_object_or_404(Outfit, id=id)
        favourites, _ = FavouriteOutfits.objects.get_or_create(user=request.user)

        if outfit in favourites.outfits.all():
            favourites.outfits.remove(outfit)
        else:
            favourites.outfits.add(outfit)

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("outfits:outfits_list")


# -------- STYLE BOARD VIEWS --------- #


class StyleBoardListView(
    IsUserOwnerMixin, LoginRequiredMixin, SetPaginateByMixin, ListView
):
    model = StyleBoard
    template_name = "outfits/styleboards/styleboard_list.html"
    context_object_name = "boards"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Style Boards"
        context["paginate_by"] = self.get_paginate_by(self.get_queryset())
        return context


class StyleBoardDetailView(IsUserOwnerMixin, LoginRequiredMixin, DetailView):
    model = StyleBoard
    template_name = "outfits/styleboards/styleboard_details.html"
    context_object_name = "board"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.object.title
        context["board_outfits"] = self.object.outfits.prefetch_related(
            "garments"
        ).all()
        return context


class StyleBoardCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "outfits.can_create_styleboard"
    model = StyleBoard
    form_class = StyleBoardCreateForm
    template_name = "outfits/styleboards/styleboard_form.html"

    def handle_no_permission(self):
        messages.error(
            self.request, "Style boards are available for Premium members only."
        )
        return redirect("outfits:styleboard_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("outfits:styleboard_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Style Board"
        context["is_create"] = True
        return context


class StyleBoardEditView(IsUserOwnerMixin, LoginRequiredMixin, UpdateView):
    model = StyleBoard
    form_class = StyleBoardEditForm
    template_name = "outfits/styleboards/styleboard_form.html"
    context_object_name = "board"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("outfits:styleboard_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit {self.object.title}"
        context["is_create"] = False
        return context


class StyleBoardDeleteView(IsUserOwnerMixin, LoginRequiredMixin, DeleteView):
    model = StyleBoard
    template_name = "outfits/styleboards/styleboard_confirm_delete.html"
    context_object_name = "board"
    success_url = reverse_lazy("outfits:styleboard_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Delete {self.object.title}"
        return context
