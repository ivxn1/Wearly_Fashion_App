from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.timezone import localdate

from outfits.models import Outfit
from planner.models import PlanEntry
from wardrobe.models import Garment


# Create your views here.

def home_view(request: HttpRequest) -> HttpResponse:
    newest_garments = Garment.objects.select_related('category', 'brand').order_by('-created_at')[:6]
    newest_outfits = Outfit.objects.select_related('occasion').order_by('-created_at')[:4]
    future_planned = PlanEntry.objects.select_related('outfit').filter(date__gte=localdate()).order_by('date')[:6]

    context = {
        'page_title': 'Wearly Home',
        'garments': newest_garments,
        'outfits': newest_outfits,
        'plans': future_planned,
    }

    return render(request, 'core/home.html', context)


def about_view(request: HttpRequest) -> HttpResponse:
    main_text = 'Wearly is a lightweight outfit planning web application that helps you stay organized when it comes to clothing and daily outfit choices.'
    secondary_text = 'Instead of keeping outfits in your head or scattered notes, Wearly lets you store garments, create outfits from them, and plan what to wear for upcoming days — all in one place.'
    contacts = 'If you have questions or suggestions, feel free to reach out at:'
    email = 'contact@wearly.app'

    context = {
        'main': main_text,
        'secondary': secondary_text,
        'contacts': contacts,
        'email': email
    }

    return render(request, 'core/about.html', context)