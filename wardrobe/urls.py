from django.urls import path

import wardrobe.views

urlpatterns = [
    path('garments/', wardrobe.views.garment_list_view, name='garment_list'),
    path('garments/<int:pk>/', wardrobe.views.garment_details, name='garment_details')
]