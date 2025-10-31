from django.urls import path
from .views import HomePageView, RestaurantListView, RestaurantDetailView, RegisterView, UserProfileView, UserProfileEditView, UserBookmarksListView, UserBookmarkToggleView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name="register"),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
    path('bookmarks/', UserBookmarksListView.as_view(), name='bookmarks_list'),
    path('bookmarks/toggle/<int:restaurant_id>/', UserBookmarkToggleView.as_view(), name='bookmark_toggle'),
]
