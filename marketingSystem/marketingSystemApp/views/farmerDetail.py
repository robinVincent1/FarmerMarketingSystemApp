from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import ProductForm, RequestForm
from ..models import FarmerProduct, Product, Request, Transaction

@login_required
def farmer_product_detail(request, farm_id):
    """
    View to display the details of a farmer's product, including products,
    pending requests, accepted requests, and transactions.
    """
    # Get the specific FarmerProduct associated with the logged-in user
    farmer_product = get_object_or_404(FarmerProduct, id=farm_id, user=request.user)
    # Get all products related to the FarmerProduct
    products = farmer_product.products.all()
    # Get all pending requests for the FarmerProduct
    requests = Request.objects.filter(id_product__farmer_product=farmer_product, request_status="Waiting").order_by('-date_request')
    # Get all accepted requests for the FarmerProduct
    accepted_requests = Request.objects.filter(id_product__farmer_product=farmer_product, request_status="Accepted").order_by('-date_request')
    # Get all transactions related to the accepted requests
    transactions = Transaction.objects.filter(id_request__in=accepted_requests)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, prefix="product")
        request_form = RequestForm(request.POST, prefix="req")

        if 'product_submit' in request.POST and product_form.is_valid():
            # Save the new product linked to the farmer's product
            product = product_form.save(commit=False)
            product.farmer_product = farmer_product
            product.save()
            messages.success(request, 'Product successfully added to the farm.')
            return redirect('farmer_product_detail', farm_id=farm_id)

        elif 'request_submit' in request.POST and request_form.is_valid():
            # Save the new request linked to the current user
            new_request = request_form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            messages.success(request, 'Request successfully submitted.')
            return redirect('farmer_product_detail', farm_id=farm_id)
    else:
        product_form = ProductForm(prefix="product")
        request_form = RequestForm(prefix="req")

    return render(request, 'farmer_product_detail.html', {
        'farmer_product': farmer_product,
        'product_form': product_form,
        'request_form': request_form,
        'products': products,
        'requests': requests,
        'transactions': transactions,
    })

@login_required
def edit_product(request, product_id):
    """
    View to edit a specific product associated with the current user.
    """
    # Get the specific Product associated with the logged-in user
    product = get_object_or_404(Product, id=product_id, farmer_product__user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated')
            return redirect('farmer_product_detail', farm_id=product.farmer_product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    """
    View to delete a specific product associated with the current user.
    """
    # Get the specific Product associated with the logged-in user
    product = get_object_or_404(Product, id=product_id, farmer_product__user=request.user)
    # Get the farm_id before deleting the product
    farm_id = product.farmer_product.id
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('farmer_product_detail', farm_id=farm_id)
