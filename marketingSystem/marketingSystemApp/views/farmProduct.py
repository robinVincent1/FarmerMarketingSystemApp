from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .form import FarmerProductForm
from ..models import FarmerProduct, Product

@login_required
def add_farmer_product(request):
    """
    View to add a new farmer product. The form is displayed and processed here.
    """
    form = FarmerProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        farmer_product = form.save(commit=False)
        farmer_product.user = request.user  # Set the logged-in user as the owner of the farmer product

        # Ensure the product is valid or null
        product_id = form.cleaned_data.get('id_product')
        if product_id:
            try:
                # Try to get the product by its ID
                product = Product.objects.get(id=product_id)
                farmer_product.id_product = product
            except Product.DoesNotExist:
                # If the product does not exist, add an error to the form
                form.add_error('id_product', 'Invalid product.')
                farmer_products = FarmerProduct.objects.all()
                return render(request, 'add_farmer_product.html', {'form': form, 'farmer_products': farmer_products})

        # Save the farmer product
        farmer_product.save()
        return redirect('home')  # Redirect to the 'home' view after creation
    else:
        if request.method == 'POST':
            print("Form error:", form.errors)  # Print form errors if the form is not valid

    # Retrieve and send the list of farmer products to each view call
    farmer_products = FarmerProduct.objects.all()
    return render(request, 'add_farmer_product.html', {'form': form, 'farmer_products': farmer_products})
