from django.shortcuts import render
from ..models import FarmerProduct, Request

def list_farms(request):
    """
    View to list all farms and the requests made by the logged-in user.
    """
    # Retrieve all farms for display
    farms = FarmerProduct.objects.all()  # Fetching farms for display

    # Retrieve requests made by the logged-in user
    user_requests = Request.objects.filter(user=request.user).order_by('-date_request')  # Ensure the Request model has a 'user' field

    context = {
        'farms': farms,
        'user_requests': user_requests,
    }
    return render(request, 'list_farms.html', context)
