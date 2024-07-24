from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .form import FinancingOfferForm
from ..models import FinancingOffer, FinancingRequest, Recommandation

def is_funder(user):
    """
    Check if the user has the 'funder' role.
    """
    return user.role == 'funder'

@login_required
@user_passes_test(is_funder, login_url='/', redirect_field_name=None)
def create_financing_offer(request):
    """
    View to create a new financing offer.
    """
    if request.method == 'POST':
        form = FinancingOfferForm(request.POST)
        if form.is_valid():
            financing_offer = form.save(commit=False)
            financing_offer.user = request.user  # Set the logged-in user
            financing_offer.save()
            messages.success(request, 'Financing offer created successfully!')
            return redirect('financing-offer')  # Adjust the redirect as needed
    else:
        form = FinancingOfferForm()

    # Get all financing offers made by the current user
    offers = FinancingOffer.objects.filter(user=request.user).prefetch_related('financingrequest_set__recommendations')

    context = {
        'form': form,
        'offers': offers
    }

    return render(request, 'financing_offer.html', context)

@login_required
@user_passes_test(is_funder, login_url='/', redirect_field_name=None)
def edit_financing_offer(request, offer_id):
    """
    View to edit an existing financing offer.
    """
    offer = get_object_or_404(FinancingOffer, id=offer_id, user=request.user)
    
    if request.method == 'POST':
        form = FinancingOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Financing offer updated successfully!')
            return redirect('financing-offer')
    else:
        form = FinancingOfferForm(instance=offer)

    context = {
        'form': form,
        'offer': offer
    }

    return render(request, 'edit_financing_offer.html', context)

@login_required
@user_passes_test(is_funder, login_url='/', redirect_field_name=None)
def delete_financing_offer(request, offer_id):
    """
    View to delete an existing financing offer.
    """
    if request.method == 'POST':
        offer = get_object_or_404(FinancingOffer, id=offer_id, user=request.user)
        offer.delete()  # This will also delete all related requests and recommendations if models are set with on_delete=models.CASCADE
        messages.success(request, 'Financing offer deleted successfully!')
        return redirect('financing-offer')
    else:
        return redirect('financing-offer')  # Redirect if the method is not POST
