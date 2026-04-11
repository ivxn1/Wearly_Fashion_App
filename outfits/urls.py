from django.urls import include, path

from outfits.views import (
    AddOutfitView,
    DeleteOutfitView,
    EditOutfitView,
    OutfitDetailsView,
    OutfitsListView,
    StyleBoardCreateView,
    StyleBoardDeleteView,
    StyleBoardDetailView,
    StyleBoardEditView,
    StyleBoardListView,
)

app_name = "outfits"

urlpatterns = [
    path(
        "outfits/",
        include(
            [
                path("", OutfitsListView.as_view(), name="outfits_list"),
                path("add/", AddOutfitView.as_view(), name="add_outfit"),
                path(
                    "<int:id>/",
                    include(
                        [
                            path(
                                "", OutfitDetailsView.as_view(), name="outfit_details"
                            ),
                            path("edit/", EditOutfitView.as_view(), name="edit_outfit"),
                            path(
                                "delete/",
                                DeleteOutfitView.as_view(),
                                name="confirm_delete_outfit",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path(
        "styleboards/",
        include(
            [
                path("", StyleBoardListView.as_view(), name="styleboard_list"),
                path("create/", StyleBoardCreateView.as_view(), name="styleboard_create"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", StyleBoardDetailView.as_view(), name="styleboard_detail"),
                            path("edit/", StyleBoardEditView.as_view(), name="styleboard_edit"),
                            path("delete/", StyleBoardDeleteView.as_view(), name="styleboard_delete"),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
