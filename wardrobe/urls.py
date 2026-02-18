from django.urls import path, include

import wardrobe.views

app_name = 'wardrobe'

urlpatterns = [
    # ------ Garment URLs ------ #
    path('garments/', include([
        path('', wardrobe.views.GarmentListView.as_view(), name='garment_list'),
        path('create/', wardrobe.views.GarmentCreateView.as_view(), name='garment_create'),
        path('<slug:slug>/', include([
            path('', wardrobe.views.GarmentDetailsView.as_view(), name='garment_details'),
            path('edit/', wardrobe.views.GarmentEditView.as_view(), name='garment_edit'),
            path('delete/', wardrobe.views.GarmentDeleteView.as_view(), name='garment_delete'),
        ]))
    ])
         ),
    # ------ Brand URLs ------ #
    path('brands/', include([
        path('', wardrobe.views.BrandListView.as_view(), name='brand_list'),
        path('create/', wardrobe.views.BrandCreateView.as_view(), name='brand_create'),
        path('<int:pk>/', include([
            path('', wardrobe.views.BrandDetailsView.as_view(), name='brand_details'),
            path('edit/', wardrobe.views.BrandEditView.as_view(), name='brand_edit'),
            path('delete/', wardrobe.views.BrandDeleteView.as_view(), name='brand_delete'),
        ])),
    ])
         )
]
