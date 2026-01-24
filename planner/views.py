from django.shortcuts import render
from planner.models import PlanEntry
# Create your views here.

app_name = 'planner'

def planner_list(request):
    plans = PlanEntry.objects.prefetch_related('outfit').order_by('date')
    return render(request, 'planner/planner_list.html', {'plans': plans, 'page_title': 'Wearly Planner'})