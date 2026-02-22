"""
Views for the planner application.

This module contains class-based views for managing outfit plan entries,
including list, detail, create, update, and delete operations.
"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from core.mixin import SetPaginateByMixin
from planner.forms import PlanCreateForm, PlanSearchForm
from planner.models import PlanEntry


class PlannerListView(SetPaginateByMixin, ListView, FormView):
    """
    Display a paginated list of plan entries with search functionality.

    Supports filtering by date and note content.
    """

    model = PlanEntry
    template_name = 'planner/planner_list.html'
    context_object_name = 'plans'
    paginate_by = 6
    form_class = PlanSearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET
        return kwargs

    def get_queryset(self):
        qs = PlanEntry.objects.prefetch_related('outfit').order_by('date')
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            if data.get('date'):
                qs = qs.filter(date=data['date'])
            if data.get('note'):
                qs = qs.filter(note__icontains=data['note'])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Wearly Planner'
        context['form'] = self.get_form()
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        return context


class PlanDetailsView(DetailView):
    """
    Display detailed information about a single plan entry.

    Includes navigation to previous and next plan entries.
    """

    model = PlanEntry
    template_name = 'planner/plan_entry_details.html'
    context_object_name = 'plan_entry'

    def get_queryset(self):
        return PlanEntry.objects.prefetch_related('outfit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Plan for {self.object.date}'
        context['prev_plan'] = PlanEntry.objects.filter(date__lt=self.object.date).order_by('-date').first()
        context['next_plan'] = PlanEntry.objects.filter(date__gt=self.object.date).order_by('date').first()
        return context


class AddPlanEntryView(CreateView):
    """Handle the creation of new plan entries with outfit selection."""

    model = PlanEntry
    form_class = PlanCreateForm
    template_name = 'planner/plan_entry_add_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Plan Entry'
        return context

    def get_success_url(self):
        return reverse_lazy('planner:plan_details', kwargs={'pk': self.object.pk})


class EditPlanEntryView(UpdateView):
    """Handle updating existing plan entry information."""

    model = PlanEntry
    form_class = PlanCreateForm
    template_name = 'planner/plan_entry_edit_form.html'
    context_object_name = 'plan_entry'

    def get_queryset(self):
        return PlanEntry.objects.select_related('outfit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit Plan Entry - {self.object.date}'
        return context

    def get_success_url(self):
        return reverse_lazy('planner:plan_details', kwargs={'pk': self.object.pk})


class DeletePlanEntryView(DeleteView):
    """Handle plan entry deletion with confirmation."""

    model = PlanEntry
    template_name = 'planner/plan_entry_delete_form.html'
    context_object_name = 'plan_entry'
    success_url = reverse_lazy('planner:planner_list')

    def get_queryset(self):
        return PlanEntry.objects.select_related('outfit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete Plan Entry - {self.object.date}'
        return context
