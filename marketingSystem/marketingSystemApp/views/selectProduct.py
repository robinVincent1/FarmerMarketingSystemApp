from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import RequestForm, ProductSearchForm
from ..models import FarmerProduct, Product, Request
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlencode
from geopy.distance import geodesic
from math import sqrt
from django.db.models import Q, F
from django.utils.timezone import now

@login_required
def select_product(request):
    """
    View to allow users to select a product with various filter options.
    """
    product_names = Product.objects.values_list('product_name', flat=True).distinct()
    user_requests = Request.objects.filter(user=request.user).select_related('id_product', 'id_product__farmer_product', 'id_product__farmer_product__user')

    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data.get('product_name', '')
            date_filter = form.cleaned_data.get('date', '')
            price_filter = form.cleaned_data.get('price', 0)
            volume_filter = form.cleaned_data.get('volume', 0)
            latitude = form.cleaned_data.get('latitude', 0)
            longitude = form.cleaned_data.get('longitude', 0)
            quality_filter = form.cleaned_data.get('quality', '')
            production_method_filter = form.cleaned_data.get('production_method', '')
            certifications_filter = form.cleaned_data.get('certifications', '')

            params = {
                'product_name': product_name,
                'date': date_filter,
                'price': price_filter,
                'volume': volume_filter,
                'latitude': latitude,
                'longitude': longitude,
                'quality': quality_filter,
                'production_method': production_method_filter,
                'certifications': certifications_filter,
            }
            url = reverse('list_farms_for_product')
            query_string = urlencode(params)
            return redirect(f"{url}?{query_string}")
    else:
        form = ProductSearchForm()

    return render(request, 'select_product.html', {
        'form': form,
        'product_names': product_names,
        'user_requests': user_requests
    })

def list_farms_for_product(request):
    """
    View to list farms based on product search criteria.
    """
    product_name = request.GET.get('product_name')
    date_filter = request.GET.get('date')
    price_filter = request.GET.get('price')
    volume_filter = request.GET.get('volume')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    quality_filter = request.GET.get('quality')
    production_method_filter = request.GET.get('production_method')
    certifications_filter = request.GET.get('certifications')

    farms = FarmerProduct.objects.all()

    def euclidean_distance(farm):
        """
        Calculate the Euclidean distance for sorting farms based on search criteria.
        """
        distance = Decimal(0)
        if product_name and farm.products.filter(product_name__icontains=product_name).exists():
            distance += Decimal(0)
        if date_filter:
            if farm.season_start and farm.season_end:
                need_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                if farm.season_start <= need_date <= farm.season_end:
                    distance += Decimal(0)
                else:
                    distance += Decimal(1)
        if price_filter:
            distance += (farm.price - Decimal(price_filter)) ** 2
        if volume_filter:
            remaining_volume = farm.remaining_volume if farm.remaining_volume else 0
            distance += (Decimal(remaining_volume) - Decimal(volume_filter)) ** 2
        if quality_filter and farm.quality == quality_filter:
            distance += Decimal(0)
        if production_method_filter and farm.production_method == production_method_filter:
            distance += Decimal(0)
        if certifications_filter and certifications_filter in farm.certifications:
            distance += Decimal(0)
        if latitude and longitude:
            user_location = (float(latitude), float(longitude))
            farm_location = (farm.latitude, farm.longitude)
            distance += Decimal(geodesic(user_location, farm_location).kilometers) ** 2

        return sqrt(float(distance))

    farms = sorted(farms, key=euclidean_distance)

    context = {
        'farms': farms,
        'product_name': product_name,
        'quantity': volume_filter if volume_filter else 1,
        'need_date': date_filter if date_filter else '',
        'price': price_filter if price_filter else 0,
        'latitude': latitude if latitude else '',
        'longitude': longitude if longitude else '',
        'quality': quality_filter if quality_filter else '',
        'production_method': production_method_filter if production_method_filter else '',
        'certifications': certifications_filter if certifications_filter else '',
    }

    return render(request, 'list_farms_for_product.html', context)

@login_required
def create_request(request, farm_id, product_name, quantity):
    """
    View to create a new request for a specific product from a farm.
    """
    farm = get_object_or_404(FarmerProduct, id=farm_id)
    product = get_object_or_404(Product, product_name=product_name, farmer_product=farm)

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.id_product = product
            req.request_status = 'Waiting'
            req.date_request = now()
            req.product_quality = farm.product_quality
            req.product_volume = quantity

            # Save other hidden fields
            need_date_str = request.POST.get('need_date')
            req.need_date = datetime.strptime(need_date_str, '%Y-%m-%d').date() if need_date_str and need_date_str != 'None' else None
            req.latitude = request.POST.get('latitude')
            req.longitude = request.POST.get('longitude')
            req.quality = request.POST.get('quality')
            req.production_method = request.POST.get('production_method')
            season_start_str = request.POST.get('season_start')
            req.season_start = datetime.strptime(season_start_str, '%Y-%m-%d').date() if season_start_str and season_start_str != 'None' else None
            season_end_str = request.POST.get('season_end')
            req.season_end = datetime.strptime(season_end_str, '%Y-%m-%d').date() if season_end_str and season_end_str != 'None' else None
            req.certifications = request.POST.get('certifications')

            # Calculate and set the total price
            req.total_price = form.cleaned_data['price'] * req.product_volume
            
            req.save()
            messages.success(request, 'Votre demande a été soumise avec succès.')
            return redirect('list_farms')
    else:
        form = RequestForm()

    return render(request, 'create_request.html', {
        'form': form,
        'farm': farm,
        'product': product,
        'quantity': quantity,
        'need_date': request.GET.get('need_date'),
        'latitude': request.GET.get('latitude'),
        'longitude': request.GET.get('longitude'),
        'quality': request.GET.get('quality'),
        'production_method': request.GET.get('production_method'),
        'season_start': request.GET.get('season_start'),
        'season_end': request.GET.get('season_end'),
        'certifications': request.GET.get('certifications'),
    })
