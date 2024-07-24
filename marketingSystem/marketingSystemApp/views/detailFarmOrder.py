from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .form import RequestForm
from ..models import FarmerProduct, Request

@login_required
def farm_detail(request, farm_id):
    # Get the specific farm product using the provided farm_id
    farm = get_object_or_404(FarmerProduct, id=farm_id)
    # Get all products related to the farm
    products = farm.products.all()
    # Check if the request method is POST
    if request.method == 'POST':
        form = RequestForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user  # Set the logged-in user
            req.rating = 0  # Set the rating value to 0
            req.save()
            return redirect('list_farms')  # Redirect to the list of farms
    else:
        form = RequestForm()  # Create an empty form instance

    return render(request, 'farm_detail.html', {
        'farm': farm,
        'form': form,
        'products': products,
    })
