from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.utils.timezone import now

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    id_user = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=255)
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    FARMER = 'farmer'
    CUSTOMER = 'customer'
    FUNDER = 'funder' 
    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (CUSTOMER, 'Customer'),
        (FUNDER, 'Funder'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    age = models.PositiveIntegerField(default=25)  # Assumption: Default age is 25
    asset = models.CharField(max_length=255, default='Not specified')
    experience = models.PositiveIntegerField(default=0)  # Assumption: Default experience is 0 years
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    children_number = models.DecimalField(max_digits=10, decimal_places=2)
    certification = models.CharField(max_length=255, default='Not specified')
    
    def __str__(self):
        return self.username

    # Add unique related_names to resolve conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users_groups',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

class FinancingOffer(models.Model):
    """
    Model representing a financing offer.
    """
    id_offer = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Automatically generated ID
    offer_date = models.DateField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.DecimalField(max_digits=10, decimal_places=2)
    asset = models.CharField(max_length=255, default='Not specified', null=True)
    age = models.DecimalField(max_digits=10, decimal_places=2)
    children_number = models.DecimalField(max_digits=10, decimal_places=2)

class FinancingRequest(models.Model):
    """
    Model representing a financing request.
    """
    id_financingrequest = models.CharField(max_length=255)  # Unique identifier for the request
    offer = models.ForeignKey(FinancingOffer, on_delete=models.CASCADE)  # Offer associated with the request
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User associated with the request
    content = models.CharField(max_length=255)
    date_request = models.DateField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class FinancingApproved(models.Model):
    """
    Model representing an approved financing request.
    """
    id_financingapproved = models.CharField(max_length=255)  # Unique identifier for the approval
    request = models.ForeignKey(FinancingRequest, on_delete=models.CASCADE)  # Request associated with the approval
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User associated with the approval
    date_approved = models.DateField(null=True)

class Chatting(models.Model):
    """
    Model representing a chat between two users.
    """
    id_chat = models.CharField(max_length=255)  # Unique identifier for the chat
    id_user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1_chats')  # First user in the chat
    id_user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2_chats')  # Second user in the chat
    content = models.CharField(max_length=255)  # Content of the chat
    channel_date = models.DateField(null=True)

class Product(models.Model):
    """
    Model representing a product.
    """
    id_product = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product_name = models.CharField(max_length=255, default='Nouveau Produit')
    measurement = models.CharField(max_length=255, default='Unité')
    season_start = models.DateField(null=True, blank=True)
    season_end = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quality = models.CharField(max_length=255, default='Standard')
    production_method = models.CharField(max_length=255, default='Standard')
    certifications = models.CharField(max_length=255, null=True, blank=True)
    minimum_order_quantity = models.IntegerField(null=True, blank=True)
    farmer_product = models.ForeignKey(
        'FarmerProduct',
        on_delete=models.CASCADE,
        related_name='products'
    )

class FarmerProduct(models.Model):
    """
    Model representing a farmer's product.
    """
    id_farmproduct = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product_date = models.DateField(default=now)  # Use the current date as the default
    product_quality = models.CharField(max_length=255, default='Standard')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_volume = models.CharField(max_length=255, default='0')
    remaining_volume = models.CharField(max_length=255, default='0')
    date_available = models.DateField(null=True)  # Can remain nullable if the date is not known in advance
    rating = models.CharField(max_length=255, default="N/A")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    quality = models.CharField(max_length=50, choices=[('bio', 'Bio'), ('conventionnel', 'Conventionnel'), ('premium', 'Premium')], default='conventionnel')
    production_method = models.CharField(max_length=50, choices=[('bio', 'Biologique'), ('hydroponie', 'Hydroponie'), ('durable', 'Durable')], default='conventionnel')
    season_start = models.DateField(null=True, blank=True)
    season_end = models.DateField(null=True, blank=True)
    certifications = models.CharField(max_length=255, blank=True)  # Ensure this field is correctly defined
    minimum_order_quantity = models.PositiveIntegerField(default=1)

class Request(models.Model):
    """
    Model representing a request for a product.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    request_status = models.CharField(max_length=255, default='En attente')
    date_request = models.DateField(default=now)
    product_quality = models.CharField(max_length=255)
    product_volume = models.IntegerField()
    need_date = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()  # New field for content

    def __str__(self):
        return f"Request for {self.id_product.product_name} by {self.user.username}"

class Transaction(models.Model):
    """
    Model representing a transaction.
    """
    id_transaction = models.CharField(max_length=255)
    id_request = models.ForeignKey(Request, on_delete=models.CASCADE)
    volume = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField(null=True)

class Recommandation(models.Model):
    """
    Model representing a recommendation.
    """
    id_recommendation = models.CharField(max_length=255)  # Unique identifier for the recommendation
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User associated with the recommendation
    request = models.ForeignKey(FinancingRequest, on_delete=models.CASCADE, related_name='recommendations')  # Request associated with the recommendation
    recommendation_score = models.CharField(max_length=255)
