from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from outfits.models import Outfit
from wardrobe.models import Garment, Brand, Category


# Create your views here.

def garment_list_view(request: HttpRequest) -> HttpResponse:
    qs = Garment.objects.select_related("brand", "category").all()

    brand_id = request.GET.get("brand", "")
    category_id = request.GET.get("category", "")
    season = request.GET.get("season", "")
    q = request.GET.get("q", "")
    sort = request.GET.get("sort", "")
    page_number = request.GET.get("page", 1)

    # filtering
    if brand_id:
        qs = qs.filter(brand_id=brand_id)

    if category_id:
        qs = qs.filter(category_id=category_id)

    if season:
        qs = qs.filter(season=season)

    if q:
        qs = qs.filter(title__icontains=q)

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
        "garments": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "brands": Brand.objects.order_by("name"),
        "categories": Category.objects.order_by("name"),
        "current_brand": brand_id,
        "current_category": category_id,
        "current_season": season,
        "current_q": q,
        "current_sort": sort,
    }
    return render(request, "wardrobe/garment_list.html", context)


def garment_details(request: HttpRequest, pk:int) -> HttpResponse:
    garm = get_object_or_404(Garment, pk=pk)
    in_outfits = Outfit.objects.filter(outfitgarment__garment=garm).distinct()

    context = {
        "garment": garm,
        "in_outfits": in_outfits
    }

    return render(request, "wardrobe/garment_details.html", context)