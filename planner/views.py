from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from planner.forms import PlanCreateForm
from planner.models import PlanEntry
# Create your views here.

app_name = 'planner'

def planner_list(request):
    plans = PlanEntry.objects.prefetch_related('outfit').order_by('date')
    return render(request, 'planner/planner_list.html', {'plans': plans, 'page_title': 'Wearly Planner'})

def plan_details(request: HttpRequest, pk:int) -> HttpResponse:
    plan_entry = PlanEntry.objects.prefetch_related('outfit').get(pk=pk)
    prev_plan = PlanEntry.objects.filter(date__lt=plan_entry.date).order_by('-date').first()
    next_plan = PlanEntry.objects.filter(date__gt=plan_entry.date).order_by('date').first()

    context = {
        'page_title': f'Plan for {plan_entry.date}',
        'plan_entry': plan_entry,
        'prev_plan': prev_plan,
        'next_plan': next_plan,
    }

    return render(request, 'planner/plan_entry_details.html', context)

def add_plan_entry(request: HttpRequest) -> HttpResponse:
    form = PlanCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('planner:plan_details', pk=form.instance.pk)

    context = {
        'page_title': 'Add Plan Entry',
        'form': form,
    }
    return render(request, 'planner/plan_entry_add_form.html', context)

def edit_plan_entry(request: HttpRequest, pk:int) -> HttpResponse:
    plan_entry = PlanEntry.objects.select_related('outfit').get(pk=pk)
    form = PlanCreateForm(request.POST or None, instance=plan_entry)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('planner:plan_details', pk=plan_entry.pk)

    context = {
        'page_title': f'Edit Plan Entry - {plan_entry.date}',
        'form': form,
        'plan_entry': plan_entry,
    }

    return render(request, 'planner/plan_entry_edit_form.html', context)

def confirm_delete_plan_entry(request: HttpRequest, pk:int) -> HttpResponse:
    plan_entry = PlanEntry.objects.select_related('outfit').get(pk=pk)

    if request.method == "POST":
        plan_entry.delete()
        return redirect('planner:planner_list')

    context = {
        'page_title': f'Delete Plan Entry - {plan_entry.date}',
        'plan_entry': plan_entry,
    }

    return render(request, 'planner/plan_entry_delete_form.html', context)