from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from outfits.models import Outfit
from wardrobe.choices import GARMENT_CATEGORY_CHOICES
from wardrobe.forms import GarmentSearchForm, GarmentCreateForm, BrandCreateForm
from wardrobe.models import Garment, Brand


# Create your views here.

# -------- GARMENT VIEWS --------- #

def garment_list_view(request: HttpRequest) -> HttpResponse:
    garments = Garment.objects.select_related("brand").all()

    form = GarmentSearchForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data.get('brand'):
            garments = garments.filter(brand=form.cleaned_data['brand'])
        if form.cleaned_data.get('category'):
            garments = garments.filter(category=form.cleaned_data['category'])
        if form.cleaned_data.get('season'):
            garments = garments.filter(season=form.cleaned_data['season'])
        if form.cleaned_data.get('title'):
            garments = garments.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data.get('sort') == 'price_asc':
            garments = garments.order_by('price')
        elif form.cleaned_data.get('sort') == 'price_desc':
            garments = garments.order_by('-price')
        elif form.cleaned_data.get('sort') == 'newest':
            garments = garments.order_by('-created_at')

    page_number = request.GET.get("page", 1)

    # pagination
    paginator = Paginator(garments, 12)
    page_obj = paginator.get_page(page_number)

    context = {
        "wardrobe": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        'page_title': 'Wearly Wardrobe',
        'form': form
    }
    return render(request, "wardrobe/garments/garments_list.html", context)


def garment_details(request: HttpRequest, slug:str) -> HttpResponse:
    garm = get_object_or_404(Garment, slug=slug)
    in_outfits = Outfit.objects.filter(outfitgarment__garment=garm).distinct()

    context = {
        'page_title': f'Garment Details - {garm.title}',
        "garment": garm,
        "in_outfits": in_outfits
    }

    return render(request, "wardrobe/garments/garment_details.html", context)

def create_garment(request: HttpRequest) -> HttpResponse:
    form = GarmentCreateForm(request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('wardrobe:garment_list')

    context = {
        'page_title': 'Add Garment',
        'form': form,
    }

    return render(request, 'wardrobe/garments/garment_add_form.html', context)


def garment_confirm_delete(request:HttpRequest, slug:str) -> HttpResponse:
    garm = get_object_or_404(Garment, slug=slug)

    if request.method == 'POST':
        garm.delete()
        return redirect('wardrobe:garment_list')

    return render(request, 'wardrobe/garments/garment_confirm_delete.html', {'garment': garm})

def edit_garment(request:HttpRequest, slug:str) -> HttpResponse:
    garm = get_object_or_404(Garment, slug=slug)
    form = GarmentCreateForm(request.POST or None, instance=garm, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('wardrobe:garment_details', slug=garm.slug)

    context = {
        'page_title': f'Edit Garment - {garm.title}',
        'garment': garm,
        'form': form,
    }

    return render(request, 'wardrobe/garments/garment_edit_form.html', context)

# --------- BRAND VIEWS --------- #

def brand_list_view(request:HttpRequest) -> HttpResponse:
    brands = Brand.objects.annotate(
        garment_count=Count('wardrobe')
    ).order_by('name').all()

    most_used_in_outfits = Brand.objects.annotate(
        outfit_count=Count('wardrobe__outfitgarment__outfit', distinct=True)
    ).order_by('-outfit_count').first()

    most_expensive_brand = Brand.objects.annotate(
        avg_price=Avg('wardrobe__price')
    ).filter(avg_price__isnull=False).order_by('-avg_price').first()

    most_garments_brand = brands.order_by('-garment_count').first()

    context = {
        'page_title': 'Brands',
        'brands': brands,
        'most_used_in_outfits': most_used_in_outfits,
        'most_expensive_brand': most_expensive_brand,
        'most_garments_brand': most_garments_brand,
    }

    return render(request, 'wardrobe/brands/brand_list.html', context)

def brand_details_view(request:HttpRequest, pk:int) -> HttpResponse:
    brand = Brand.objects.filter(pk=pk).annotate(
        garment_count=Count('wardrobe')).first()

    context = {
        'page_title': f'Brand Details - {brand.name}',
        'brand': brand,
    }

    return render(request, 'wardrobe/brands/brand_details.html', context)

def brand_create_view(request:HttpRequest) -> HttpResponse:
    form = BrandCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('wardrobe:brand_list')

    context = {
        'page_title': 'Add Brand',
        'form': form,
    }

    return render(request, 'wardrobe/brands/brand_add_form.html', context)

def brand_edit_view(request:HttpRequest, pk:int) -> HttpResponse:
    brand = get_object_or_404(Brand, pk=pk)
    form = BrandCreateForm(request.POST or None, instance=brand)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('wardrobe:brand_details', pk=brand.pk)

    context = {
        'page_title': f'Edit Brand - {brand.name}',
        'brand': brand,
        'form': form,
    }

    return render(request, 'wardrobe/brands/brand_edit_form.html', context)

def brand_delete_view(request:HttpRequest, pk:int) -> HttpResponse:
    brand = Brand.objects.filter(pk=pk).annotate(
        garment_count=Count('wardrobe')).first()

    if request.method == 'POST':
        brand.delete()
        return redirect('wardrobe:brand_list')

    return render(request, 'wardrobe/brands/brand_confirm_delete.html', {'brand': brand})