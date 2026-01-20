from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from outfits.models import Outfit


# Create your views here.
def outfits_list(request: HttpRequest) -> HttpResponse:
    outfits = Outfit.objects.select_related('occasion').prefetch_related('garments')

    context = {
        'page_title': 'Wearly Outfits',
        'outfits': outfits,
    }

    return render(request, 'outfits/outfits_list.html', context)