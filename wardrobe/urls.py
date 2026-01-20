from django.urls import path

import wardrobe.views

app_name = 'wardrobe'

urlpatterns = [
    path('garments/', wardrobe.views.garment_list_view, name='garment_list'),
    path('garment/<slug:slug>/', wardrobe.views.garment_details, name='garment_details'),
    path('garment/<slug:slug>/delete/', wardrobe.views.garment_confirm_delete, name='garment_confirm_delete'),
]