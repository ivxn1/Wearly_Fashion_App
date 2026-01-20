from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from outfits.models import Outfit
from wardrobe.models import Garment, Brand


# Create your views here.

def garment_list_view(request: HttpRequest) -> HttpResponse:
    qs = Garment.objects.select_related("brand").all()

    brand_id = request.GET.get("brand", "")
    category = request.GET.get("category", "")
    season = request.GET.get("season", "")
    title = request.GET.get("title", "")
    sort = request.GET.get("sort", "")
    page_number = request.GET.get("page", 1)

    # filtering
    if brand_id:
        qs = qs.filter(brand_id=brand_id)

    if category:
        qs = qs.filter(category=category)

    if season:
        qs = qs.filter(season=season)

    if title:
        qs = qs.filter(title__icontains=title)

    # sorting
    if sort == "price_asc":
        qs = qs.order_by("price", "-id")
    elif sort == "price_desc":
        qs = qs.order_by("-price", "-id")
    else:
        qs = qs.order_by("-created_at")

    # pagination
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(page_number)

    context = {
        "wardrobe": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "brands": Brand.objects.order_by("name"),
        "category_choices": Garment.CATEGORY_CHOICES,
        "current_brand": brand_id,
        "current_category": category,
        "current_season": season,
        "current_title": title,
        "current_sort": sort,
        'page_title': 'Wearly Wardrobe',
    }
    return render(request, "wardrobe/garments_list.html", context)


def garment_details(request: HttpRequest, slug:str) -> HttpResponse:
    garm = get_object_or_404(Garment, slug=slug)
    in_outfits = Outfit.objects.filter(outfitgarment__garment=garm).distinct()

    context = {
        'page_title': f'Garment Details - {garm.title}',
        "garment": garm,
        "in_outfits": in_outfits
    }

    return render(request, "wardrobe/garment_details.html", context)

def garment_confirm_delete(request:HttpRequest, slug:str) -> HttpResponse:
    garm = get_object_or_404(Garment, slug=slug)

    if request.method == 'POST':
        garm.delete()
        return redirect('garment_list')

    return render(request, 'wardrobe/garment_confirm_delete.html', {'garment': garm})