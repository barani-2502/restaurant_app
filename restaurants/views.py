from django.views.generic import ListView, DetailView
from .models import Restaurant


class HomePageView(ListView):
    model = Restaurant
    template_name = 'restaurants/home.html'
    context_object_name = 'spotlighted_restaurants'
    paginate_by = 6

    def get_queryset(self):
        return Restaurant.objects.filter(spotlight=True).prefetch_related('restaurant_photos')

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 6

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant_detail.html'
    content_object_name = 'restaurants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = self.object.menu_items.all()
        return context
