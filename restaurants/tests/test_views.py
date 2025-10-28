from django.test import TestCase
from django.urls import reverse
from restaurants.models import Restaurant, Cuisine, MenuItem
from django.core.paginator import Page
from django.contrib.auth import get_user_model


User = get_user_model()

class RestaurantListViewTests(TestCase):
    def setUp(self):
        cuisine = Cuisine.objects.create(name="Indian")

        for i in range(12):
            restaurant = Restaurant.objects.create(
                name=f"Restaurant{i}",
                address = f'Address{i}',
                city="chennai",
                cost_for_two=500,
                food_type="veg",
                open_status=True,
                spotlight=False,
            )
            restaurant.cuisines.add(cuisine)

    def test_list_view_status_code(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('restaurant-list'))

    def test_list_view_pagination_is_nine(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['restaurants']), 9)

    def test_second_page_contains_remaining_restaurants(self):
        response = self.client.get(reverse('restaurant-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['restaurants']), 3)

    def test_list_view_displays_restaurant_names(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertContains(response, "Restaurant0")
        self.assertContains(response, "Restaurant8")

class RestaurantDetailViewTests(TestCase):
    def setUp(self):
        self.cuisine = Cuisine.objects.create(name="Indian")
        self.restaurant = Restaurant.objects.create(
            name= "ABC",
            address = "pallavaram",
            city="chennai",
            cost_for_two=500,
            food_type="veg",
            open_status=True,
            spotlight=False,
        )
        self.restaurant.cuisines.add(self.cuisine)

        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Idli',
            price=30.0,
        )

        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Dosa',
            price=60.0,
        )

    def test_detail_view_status_code(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'restaurants/restaurant_detail.html')

    def test_detail_view_context_contains_restaurant(self):
        url = reverse('restaurant-detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.context['restaurant'], self.restaurant)
    
    def test_invalid_restaurant_returns_404_error(self):
        url = reverse('restaurant-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_register_page_loads_successfully(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "Register")

    def test_register_creates_user_with_valid_data(self):
        data = {
            'username': "user",
            'email': 'test@gamil.com', 
            'password1': 'pass12345678',
            'password2': 'pass12345678',
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username='user').exists())

    def test_register_creates_user_with_invalid_data(self):
        data = {
            'username': "user",
            'password1': 'pass12345678',
            'password2': 'pass12341234',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertFalse(User.objects.filter(username='user').exists())

class LoginAndLogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", email="test@gmail.com", password="pass12345678")
    
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
    
    def test_logout_page_redirects(self):
        self.client.login(username='user', password='pass12345678' )
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('home'))

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse("login"), {"username": "user", "password": "pass12345678"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse("login"), {"username": "user", "password": "wrong"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_logout_functionality(self):
        self.client.login(username='user', password='pass12345678' )
        self.client.get(reverse('logout'), follow=True)
        response = self.client.get(reverse("home"))
        self.assertFalse(response.context["user"].is_authenticated)

