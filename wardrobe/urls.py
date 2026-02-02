from django.urls import path, include

import wardrobe.views

app_name = 'wardrobe'

urlpatterns = [
    # ------ Garment URLs ------ #
    path('garments/', include([
        path('', wardrobe.views.garment_list_view, name='garment_list'),
        path('create/', wardrobe.views.create_garment, name='garment_create'),
        path('<slug:slug>/', include([
            path('', wardrobe.views.garment_details, name='garment_details'),
            path('edit/', wardrobe.views.edit_garment, name='garment_edit'),
            path('delete/', wardrobe.views.garment_confirm_delete, name='garment_delete'),
        ]))
    ])
         ),
    # ------ Brand URLs ------ #
    path('brands/', include([
        path('', wardrobe.views.brand_list_view, name='brand_list'),
        path('create/', wardrobe.views.brand_create_view, name='brand_create'),
        path('<int:pk>/', include([
            path('', wardrobe.views.brand_details_view, name='brand_details'),
            path('edit/', wardrobe.views.brand_edit_view, name='brand_edit'),
            path('delete/', wardrobe.views.brand_delete_view, name='brand_delete'),
        ])),
    ])
         )
]
