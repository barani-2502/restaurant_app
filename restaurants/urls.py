from django.urls import path
from .views import HomePageView, RestaurantListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
]
