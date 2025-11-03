from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, Bookmark
from .forms import CustomUserCreationForm, UserProfileForm


class HomePageView(ListView):
    model = Restaurant
    template_name = 'restaurants/home.html'
    context_object_name = 'spotlighted_restaurants'
    paginate_by = 9

    def get_queryset(self):
        return Restaurant.objects.filter(spotlight=True).prefetch_related('restaurant_photos')

class RestaurantListView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 9

    def get_queryset(self):
        return Restaurant.objects.prefetch_related('restaurant_photos')
    
class RestaurantDetailView(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant_detail.html'
    context_object_name = 'restaurant'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('restaurant_photos', 'cuisines')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = self.object.menu_items.prefetch_related('menu_item_photos').all()
        return context

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully")
        return response

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully")
        return super().form_valid(form)

class UserBookmarksListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'users/bookmarks_list.html'
    context_object_name = 'bookmarked_restaurants'
    paginate_by = 9

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('restaurant').prefetch_related('restaurant__restaurant_photos')
