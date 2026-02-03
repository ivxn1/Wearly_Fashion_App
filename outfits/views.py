from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from outfits.forms import OutfitCreateForm
from outfits.models import Outfit


# Create your views here.
def outfits_list(request: HttpRequest) -> HttpResponse:
    outfits = Outfit.objects.prefetch_related('garments')

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

def add_outfit(request: HttpRequest) -> HttpResponse:
    form = OutfitCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('outfits:outfit_details', id=form.instance.id)

    context = {
        'page_title': 'Add Outfit',
        'form': form,
    }

    return render(request, 'outfits/outfit_add_form.html', context)

def edit_outfit(request: HttpRequest, id:int) -> HttpResponse:
    outfit = get_object_or_404(Outfit, id=id)
    form = OutfitCreateForm(request.POST or None, instance=outfit, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('outfits:outfit_details', id=form.instance.id)

    context = {
        'page_title': f'Edit {outfit.title}',
        'form': form,
        'outfit': outfit,
    }

    return render(request, 'outfits/outfit_edit_form.html', context)

def confirm_delete_outfit(request: HttpRequest, id:int) -> HttpResponse:
    outfit = get_object_or_404(Outfit, id=id)
    if request.method == "POST":
        outfit.delete()
        return redirect('outfits:outfits_list')

    context = {
        'page_title': f'Delete {outfit.title}',
        'outfit': outfit,
    }

    return render(request, 'outfits/outfit_confirm_delete.html', context)