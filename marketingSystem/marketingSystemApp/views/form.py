from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import CustomUser, FarmerProduct, Product, Request, FinancingOffer, FinancingRequest

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new custom user, inheriting from UserCreationForm.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'gender', 'role', 'age', 'asset', 'salary', 'children_number', 'certification', 'experience', 'password1', 'password2')

class UserLoginForm(forms.Form):
    """
    Form for user login with username and password fields.
    """
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class FarmerProductForm(forms.ModelForm):
    """
    Form for creating or updating FarmerProduct instances.
    """
    class Meta:
        model = FarmerProduct
        fields = ['product_date', 'product_quality', 'price', 'product_volume', 'remaining_volume', 'date_available', 'latitude', 'longitude', 'quality', 'production_method', 'season_start', 'season_end', 'certifications', 'minimum_order_quantity']

class ProductForm(forms.ModelForm):
    """
    Form for creating or updating Product instances.
    """
    class Meta:
        model = Product
        fields = [
            'product_name', 'measurement', 'season_start', 'season_end',
            'price', 'product_quality', 'production_method', 'certifications', 
            'minimum_order_quantity'
        ]
        widgets = {
            'season_start': forms.DateInput(attrs={'type': 'date'}),
            'season_end': forms.DateInput(attrs={'type': 'date'}),
        }

class RequestForm(forms.ModelForm):
    """
    Form for creating or updating Request instances.
    """
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="Price")
    content = forms.CharField(widget=forms.Textarea, required=True, label="Content")

    class Meta:
        model = Request
        fields = ['price', 'content']
                
class TransactionUpdateForm(forms.Form):
    """
    Form for updating a transaction's product quality and rating.
    """
    product_quality = forms.CharField(max_length=255)
    rating = forms.DecimalField(max_digits=2, decimal_places=1)
    transaction_id = forms.IntegerField(widget=forms.HiddenInput())

class FinancingOfferForm(forms.ModelForm):
    """
    Form for creating or updating FinancingOffer instances.
    """
    class Meta:
        model = FinancingOffer
        exclude = ['id_offer', 'user']  # Exclude id_offer and user
        widgets = {
            'offer_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FinancingRequestForm(forms.ModelForm):
    """
    Form for creating or updating FinancingRequest instances.
    """
    class Meta:
        model = FinancingRequest
        fields = ['content', 'price']  # Assuming 'content' is what you want users to fill out, and 'price' is automatically fetched but editable.

class ProductSelectionForm(forms.Form):
    """
    Form for selecting a product and specifying the quantity.
    """
    product_id = forms.ModelChoiceField(queryset=Product.objects.all(), label='Select Product')
    quantity = forms.IntegerField(label='Quantity', min_value=1)

class ProductSearchForm(forms.Form):
    """
    Form for searching products based on various criteria.
    """
    product_name = forms.ChoiceField(
        required=False,
        choices=[(product_name, product_name) for product_name in Product.objects.values_list('product_name', flat=True).distinct()],
        label="Product Name"
    )
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    volume = forms.IntegerField(required=False)
    latitude = forms.DecimalField(required=False, max_digits=9, decimal_places=6)
    longitude = forms.DecimalField(required=False, max_digits=9, decimal_places=6)
    quality = forms.ChoiceField(choices=[('', 'Any'), ('bio', 'Organic'), ('conventionnel', 'Conventional'), ('premium', 'Premium')], required=False)
    production_method = forms.ChoiceField(choices=[('', 'Any'), ('bio', 'Organic'), ('hydroponie', 'Hydroponics'), ('durable', 'Sustainable')], required=False)
    certifications = forms.CharField(required=False)
