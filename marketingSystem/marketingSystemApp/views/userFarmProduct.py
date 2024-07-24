from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import FarmerProductForm
from ..models import FarmerProduct

@login_required
def user_farmer_products(request):
    """
    View to handle the display and creation of farmer products for the logged-in user.
    """
    farmer_products = FarmerProduct.objects.filter(user=request.user)  # Get farmer products for the logged-in user

    if request.method == 'POST':
        form = FarmerProductForm(request.POST)
        if form.is_valid():
            farmer_product = form.save(commit=False)
            farmer_product.user = request.user  # Set the user of the farmer product
            farmer_product.save()
            messages.success(request, 'Farmer product added successfully.')
            return redirect('user_farmer_products')
        else:
            messages.error(request, "Form error. Please check the entered data.")

    else:
        form = FarmerProductForm()  # Create an empty form instance

    return render(request, 'user_farmer_products.html', {
        'form': form,
        'farmer_products': farmer_products
    })
