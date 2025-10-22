from django.views.generic import ListView
from .models import Restaurant

SPOTLIGHT_RESTAURANT_COUNT = 6

class HomePageView(ListView):
    model = Restaurant
    template_name = 'restaurants/home.html'
    context_object_name = 'spotlighted_restaurants'
    paginate_by = SPOTLIGHT_RESTAURANT_COUNT

    def get_queryset(self):
        return Restaurant.objects.filter(spotlight=True).prefetch_related('restaurant_photos')

