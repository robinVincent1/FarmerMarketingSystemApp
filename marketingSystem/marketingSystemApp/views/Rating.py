from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Transaction, Request, FarmerProduct
from .form import TransactionUpdateForm

@login_required
def user_transactions(request):
    """
    View to display and update user transactions.
    """
    # Retrieve transactions for the logged-in user with an accepted status
    transactions = Transaction.objects.filter(
        id_request__user=request.user,
        id_request__request_status='Accepted'
    ).select_related('id_request', 'id_request__id_product', 'id_request__id_product__farmer_product')

    if request.method == 'POST':
        form = TransactionUpdateForm(request.POST)
        if form.is_valid():
            transaction_id = request.POST.get('transaction_id')
            transaction = get_object_or_404(Transaction, pk=transaction_id)
            farmer_product = transaction.id_request.id_product.farmer_product

            # Update the product quality and rating
            farmer_product.product_quality = form.cleaned_data['product_quality']
            farmer_product.save()
            transaction.id_request.rating = form.cleaned_data['rating']
            transaction.id_request.save()

            # Calculate and update the average rating
            all_ratings = Request.objects.filter(
                id_product__farmer_product=farmer_product,
                rating__isnull=False
            ).values_list('rating', flat=True)
            average_rating = sum(map(float, all_ratings)) / len(all_ratings) if all_ratings else 0
            farmer_product.rating = average_rating
            farmer_product.save()

            messages.success(request, "Information updated successfully.")
            return redirect('user_transactions')
    else:
        form = TransactionUpdateForm()

    return render(request, 'user-transactions.html', {
        'transactions': transactions,
        'form': form
    })
