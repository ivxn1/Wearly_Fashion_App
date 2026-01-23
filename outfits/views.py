from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from outfits.models import Outfit


# Create your views here.
def outfits_list(request: HttpRequest) -> HttpResponse:
    outfits = Outfit.objects.select_related('occasion').prefetch_related('garments')

    context = {
        'page_title': 'Wearly Outfits',
        'outfits': outfits,
    }

    return render(request, 'outfits/outfits_list.html', context)

def outfit_details(request: HttpRequest, id:int) -> HttpResponse:
    outfit = get_object_or_404(Outfit, id=id)
    outfit_garments = outfit.garments.all()

    context = {
        'page_title': outfit.title,
        'outfit': outfit,
        'outfit_garments': outfit_garments,
    }

    return render(request, 'outfits/outfit_details.html', context)
