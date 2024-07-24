from django.shortcuts import render
from ..models import FinancingOffer
from django.db.models import Q, Max, Min
from datetime import datetime
from math import sqrt
from decimal import Decimal

def list_financing_offers(request):
    """
    View to list financing offers based on user's query parameters and profile.
    """
    # Retrieve GET request parameters
    date_filter = request.GET.get('date', None)
    price_filter = request.GET.get('price', None)
    
    # Convert filters to appropriate types
    if date_filter:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
    if price_filter:
        price_filter = Decimal(price_filter)

    # Filter offers based on user parameters
    if request.user.is_authenticated:
        user_salary = request.user.salary
        user_experience = request.user.experience
        user_age = request.user.age
        user_children_number = request.user.children_number

        # Retrieve all offers for comparison
        offers = FinancingOffer.objects.all()

        # Get min and max for normalization
        max_salary = offers.aggregate(Max('salary'))['salary__max']
        min_salary = offers.aggregate(Min('salary'))['salary__min']
        max_experience = offers.aggregate(Max('experience'))['experience__max']
        min_experience = offers.aggregate(Min('experience'))['experience__min']

        def normalize(value, min_value, max_value):
            return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

        normalized_user_salary = normalize(user_salary, min_salary, max_salary)
        normalized_user_experience = normalize(user_experience, min_experience, max_experience)

        def euclidean_distance(offer):
            """
            Calculate the Euclidean distance for sorting based on all filters.
            """
            distance = 0

            if date_filter:
                date_distance = (offer.offer_date - date_filter).days ** 2
                distance += date_distance

            if price_filter:
                price_distance = (offer.price - price_filter) ** 2
                distance += price_distance

            normalized_offer_salary = normalize(offer.salary, min_salary, max_salary)
            normalized_offer_experience = normalize(offer.experience, min_experience, max_experience)

            salary_distance = (normalized_offer_salary - normalized_user_salary) ** 2
            experience_distance = (normalized_offer_experience - normalized_user_experience) ** 2
            age_distance = (offer.age - user_age) ** 2
            children_distance = (offer.children_number - user_children_number) ** 2

            distance += salary_distance + experience_distance + age_distance + children_distance

            return sqrt(distance)

        # Sort offers based on Euclidean distance to the filters
        offers = sorted(offers, key=euclidean_distance)

    else:
        offers = FinancingOffer.objects.all()

    # Retrieve financing requests of the logged-in user
    user_requests = request.user.financingrequest_set.all() if request.user.is_authenticated else []

    return render(request, 'financing.html', {
        'offers': offers,
        'user_requests': user_requests
    })
