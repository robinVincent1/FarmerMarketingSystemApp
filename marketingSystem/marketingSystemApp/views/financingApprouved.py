from django.shortcuts import get_object_or_404, redirect
from ..models import FinancingRequest, FinancingApproved
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def reject_financing_request(request, request_id):
    """
    View to reject a financing request. Only superusers or the user who made the request can reject it.
    """
    if request.method == 'POST':
        # Get the specific FinancingRequest by ID
        financing_request = get_object_or_404(FinancingRequest, id=request_id)
        # Check if the user is a superuser or the owner of the request
        if request.user.is_superuser or request.user == financing_request.user:
            financing_request.delete()  # Delete the financing request
            messages.success(request, "Financing request successfully rejected.")
        else:
            messages.error(request, "You do not have permission to reject this financing request.")
        return redirect('financing-offer')  # Redirect to the financing offer view

@login_required
def accept_financing_request(request, request_id):
    """
    View to accept a financing request. Ensures that the request is not already approved.
    """
    if request.method == 'POST':
        # Get the specific FinancingRequest by ID
        financing_request = get_object_or_404(FinancingRequest, id=request_id)
        # Check if the request has not already been approved
        if not FinancingApproved.objects.filter(request=financing_request).exists():
            # Create a new FinancingApproved record
            FinancingApproved.objects.create(
                request=financing_request,
                user=request.user,
                date_approved=now()
            )
            messages.success(request, "Financing request successfully accepted.")
        else:
            messages.error(request, "This request has already been approved.")
        return redirect('financing-offer')  # Redirect to the financing offer view
