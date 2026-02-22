from django.urls import include, path

from planner.views import (
    AddPlanEntryView,
    DeletePlanEntryView,
    EditPlanEntryView,
    PlanDetailsView,
    PlannerListView,
)

app_name = "planner"

urlpatterns = [
    path(
        "planner/",
        include(
            [
                path("", PlannerListView.as_view(), name="list"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", PlanDetailsView.as_view(), name="plan_details"),
                            path(
                                "edit/",
                                EditPlanEntryView.as_view(),
                                name="edit_plan_entry",
                            ),
                            path(
                                "delete/",
                                DeletePlanEntryView.as_view(),
                                name="delete_plan_entry",
                            ),
                        ]
                    ),
                ),
                path("add/", AddPlanEntryView.as_view(), name="add_plan_entry"),
            ]
        ),
    ),
]
