from django.urls import path

from outfits.views import outfits_list, outfit_details

app_name = 'outfits'

urlpatterns = [
    path('outfits/', outfits_list, name='outfits_list'),
    path('outfits/<int:id>/', outfit_details, name='outfit_details'),
]