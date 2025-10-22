from django.urls import path
from .views import HomePageView, RestaurantListView, RestaurantDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
