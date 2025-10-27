from django.test import TestCase
from django.urls import reverse
<<<<<<< HEAD
from restaurants.models import Restaurant, Cuisine, MenuItem
=======
from restaurants.models import Restaurant, Cuisine
>>>>>>> b4cbac1 (tests: Add testcases for RestaurantListView)
from django.core.paginator import Page

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
