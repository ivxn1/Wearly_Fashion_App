from django.urls import path

from planner.views import planner_list

app_name = 'planner'

urlpatterns = [
    path('planner/', planner_list, name='list')
]