from django.urls import path

from outfits.views import outfits_list

app_name = 'outfits'

urlpatterns = [
    path('outfits/', outfits_list, name='outfits_list'),
]