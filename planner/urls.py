from django.urls import path

from planner.views import planner_list, plan_details

app_name = 'planner'

urlpatterns = [
    path('planner/', planner_list, name='list'),
    path('planner/<int:pk>/', plan_details, name='plan_details'),
]