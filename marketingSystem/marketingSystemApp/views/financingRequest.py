from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import FinancingRequestForm  # Ensure the path is correct
from ..models import FinancingOffer, FinancingRequest, Recommandation, CustomUser
from django.utils.timezone import now

@login_required
def create_financing_request(request, offer_id):
    """
    View to create a financing request for a specific offer.
    """
    offer = get_object_or_404(FinancingOffer, id=offer_id)
    user_requests = FinancingRequest.objects.filter(user=request.user).order_by('-date_request')
    
    if request.method == 'POST':
        form = FinancingRequestForm(request.POST)
        if form.is_valid():
            financing_request = form.save(commit=False)
            financing_request.offer = offer
            financing_request.user = request.user
            financing_request.date_request = now()
            financing_request.save()

            # Calculate recommendation score
            score = calculate_score(request.user)

            # Create Recommendation
            recommendation = Recommandation(
                user=request.user,
                request=financing_request,
                recommendation_score=score
            )
            recommendation.save()

            return redirect('financing')  # Redirect to an appropriate URL
    else:
        form = FinancingRequestForm()

    return render(request, 'financing_request_form.html', {
        'form': form,
        'offer': offer,
        'user_requests': user_requests  # Pass the user requests to the template
    })

def calculate_score(user):
    """
    Function to calculate a recommendation score based on user attributes.
    """
    score = 0
    if user.experience > 5:
        score += 1
    if user.asset != 'Not specified':
        score += 1
    if user.age > 30:
        score += 1
    return str(min(score, 5))  # Score out of 5
