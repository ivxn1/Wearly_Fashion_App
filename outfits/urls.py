from django.urls import path, include

from outfits.views import outfits_list, outfit_details, add_outfit, edit_outfit, confirm_delete_outfit

app_name = 'outfits'

urlpatterns = [
    path('outfits/', include([
        path('', outfits_list, name='outfits_list'),
        path('add/', add_outfit, name='add_outfit'),
        path('<int:id>/', include([
            path('', outfit_details, name='outfit_details'),
            path('edit/', edit_outfit, name='edit_outfit'),
            path('delete/', confirm_delete_outfit, name='confirm_delete_outfit'),
    ])),
    ])
         ),
]