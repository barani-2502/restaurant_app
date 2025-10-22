from django.views.generic import TemplateView
from .models import Restaurant

SPOTLIGHT_RESTAURANT_COUNT = 6

class HomePageView(TemplateView):
    template_name = 'restaurants/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spotlighted_restaurants'] = Restaurant.objects.filter(spotlight=True)[:5].prefetch_related('restaurant_photos')[:SPOTLIGHT_RESTAURANT_COUNT]
        return context

