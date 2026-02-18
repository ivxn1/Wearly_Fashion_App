from django.urls import path, include

from outfits.views import OutfitsListView, OutfitDetailsView, AddOutfitView, EditOutfitView, DeleteOutfitView

app_name = 'outfits'

urlpatterns = [
    path('outfits/', include([
        path('', OutfitsListView.as_view(), name='outfits_list'),
        path('add/', AddOutfitView.as_view(), name='add_outfit'),
        path('<int:id>/', include([
            path('', OutfitDetailsView.as_view(), name='outfit_details'),
            path('edit/', EditOutfitView.as_view(), name='edit_outfit'),
            path('delete/', DeleteOutfitView.as_view(), name='confirm_delete_outfit'),
        ])),
    ])),
]