from django.urls import path, include

import wardrobe.views

app_name = 'wardrobe'

urlpatterns = [
    path('garments/', include([
        path('', wardrobe.views.garment_list_view, name='garment_list'),
        path('create/', wardrobe.views.create_garment, name='garment_create'),
        path('<slug:slug>/', include([
            path('', wardrobe.views.garment_details, name='garment_details'),
            path('edit/', wardrobe.views.edit_garment, name='garment_edit'),
        ]))
    ])
         )
]
