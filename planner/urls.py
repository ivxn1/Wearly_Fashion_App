from django.urls import path, include

from planner.views import planner_list, plan_details, add_plan_entry, edit_plan_entry, confirm_delete_plan_entry

app_name = 'planner'

urlpatterns = [
    path('planner/', include([
        path('', planner_list, name='list'),
        path('<int:pk>/', include([
            path('', plan_details, name='plan_details'),
            path('edit/', edit_plan_entry, name='edit_plan_entry'),
            path('delete/', confirm_delete_plan_entry, name='delete_plan_entry'),
        ])),

        path('add/', add_plan_entry, name='add_plan_entry'),

    ])),
]