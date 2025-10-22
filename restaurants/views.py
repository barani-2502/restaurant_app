from django.shortcuts import render
from .models import Restaurant

SPOTLIGHT_RESTAURANT_COUNT = 5

def home(request):
    spotlighted_restaurants = Restaurant.objects.filter(spotlight=True)[:5].prefetch_related('restaurant_photos')[:SPOTLIGHT_RESTAURANT_COUNT]
    context = {
        'spotlighted_restaurants': spotlighted_restaurants
    }

    return render(request, 'restaurants/home.html', context)

