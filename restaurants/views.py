from django.shortcuts import render
from .models import Restaurant

def home(request):
    spotlighted_restaurants = Restaurant.objects.filter(spotlight=True)[:5]
    context = {
        'spotlighted_restaurants': spotlighted_restaurants
    }

    return render(request, 'restaurants/home.html', context)

