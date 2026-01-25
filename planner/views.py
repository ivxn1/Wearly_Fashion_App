from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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