from django.shortcuts import render, redirect, get_object_or_404
from ..models import Request, FarmerProduct, Transaction
from django.contrib import messages
from django.utils.timezone import now

def create_transaction(request_instance):
    transaction = Transaction(
        id_request=request_instance,
        volume=request_instance.product_volume,
        total_price=float(request_instance.product_volume) * request_instance.id_product.price,
        transaction_date=now()
    )
    transaction.save()

def accept_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    product = req.id_product
    farmer_product = product.farmer_product

    try:
        requested_volume = float(req.product_volume)
        current_farm_volume = float(farmer_product.product_volume)
        current_product_volume = float(product.measurement)  # Assurez-vous que le volume est géré comme un float

        # Vérifiez si le volume demandé est disponible
        if requested_volume <= current_farm_volume and requested_volume <= current_product_volume:
            # Mise à jour des volumes
            farmer_product.product_volume = str(current_farm_volume - requested_volume)
            product.measurement = str(current_product_volume - requested_volume)
            farmer_product.save()
            product.save()

            # Créer la transaction
            Transaction.objects.create(
                id_request=req,
                volume=req.product_volume,
                total_price=requested_volume * float(farmer_product.price),
                transaction_date=now()
            )
            req.request_status = 'Accepted'
            req.save()
            messages.success(request, 'Requête acceptée et volumes mis à jour.')
            return redirect('farmer_product_detail', farm_id=farmer_product.id)
        else:
            messages.error(request, "Volume demandé non disponible.")
            return redirect('farmer_product_detail', farm_id=farmer_product.id)

    except Exception as e:
        messages.error(request, f"Erreur lors de l'acceptation de la demande: {str(e)}")
        return redirect('farmer_product_detail', farm_id=farmer_product.id)



def reject_request(request, request_id):
    if request.method == 'POST':
        req = get_object_or_404(Request, pk=request_id)
        req.delete()  # Suppression de la requête
        return redirect('farmer_product_detail')  # Redirection après la suppression
