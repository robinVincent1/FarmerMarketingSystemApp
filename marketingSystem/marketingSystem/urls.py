from django.contrib import admin
from django.urls import path, include
from marketingSystemApp.views import signin, signup, home, farmProduct, userFarmProduct, farmerDetail, listFarm, detailFarmOrder, transaction, Rating, FunderOffer, financing, financingRequest, financingApprouved, selectProduct

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('signup/', signup.register, name='signup'),
    path('signin/', signin.login, name='signin'),
    path('home/', home.homePage, name='home'),
    path('home/add-farmer-product/', farmProduct.add_farmer_product, name='add_farmer_product'),
    path('home/mes-produits-fermiers/', userFarmProduct.user_farmer_products, name='user_farmer_products'),
    path('farmer-products/<int:farm_id>/', farmerDetail.farmer_product_detail, name='farmer_product_detail'),
    
    path('product/edit/<int:product_id>/', farmerDetail.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', farmerDetail.delete_product, name='delete_product'),
 
    path('farms/', listFarm.list_farms, name='list_farms'),  # Use this for listing farms
    path('farms/<int:farm_id>/', detailFarmOrder.farm_detail, name='farm_detail'),  # Details for a specific farm
    path('accept-request/<int:request_id>/', transaction.accept_request, name='accept_request'),
    path('reject-request/<int:request_id>/', transaction.reject_request, name='reject_request'),
    path('user-transactions/', Rating.user_transactions, name='user_transactions'),
    path('financing-offer/', FunderOffer.create_financing_offer, name='financing-offer'),
    path('financing/', financing.list_financing_offers, name='financing'),  # URL for listing financing offers with filters
    path('financing/request/<int:offer_id>/', financingRequest.create_financing_request, name='create_financing_request'),
    path('financing/request/accept/<int:request_id>/', financingApprouved.accept_financing_request, name='accept_financing_request'),
    path('financing/request/reject/<int:request_id>/', financingApprouved.reject_financing_request, name='reject_financing_request'),
    path('financing-offer/delete/<int:offer_id>/', FunderOffer.delete_financing_offer, name='delete_financing_offer'),
    path('edit-financing-offer/<int:offer_id>/', FunderOffer.edit_financing_offer, name='edit_financing_offer'),
    
    path('select_product/', selectProduct.select_product, name='select_product'),
    path('list_farms_for_product/', selectProduct.list_farms_for_product, name='list_farms_for_product'),
    path('create_request/<int:farm_id>/<str:product_name>/<int:quantity>/', selectProduct.create_request, name='create_request'),
]
