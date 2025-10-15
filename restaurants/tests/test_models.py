from django.test import TestCase
from decimal import Decimal
from restaurants.models import Cuisine, Restaurant, MenuItem, RestaurantPhoto

class ModelTest(TestCase):
    def setUp(self):
        self.cuisine = Cuisine.objects.create(name="Chinese")
        self.restaurant = Restaurant.objects.create(
            name="A2B",
            address="ABC Street",
            city = "Chennai",
            cost_for_two=300,
            food_type=Restaurant.non_veg,
        )
        self.restaurant.cuisines.add(self.cuisine)

    def test_cuisine_creation(self):
        self.assertEqual(self.cuisine.name, "Chinese")
        self.assertEqual(str(self.cuisine), "Chinese")

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "A2B")
        self.assertEqual(self.restaurant.city, "Chennai")
        self.assertTrue(self.restaurant.open_status)
        self.assertFalse(self.restaurant.spotlight)
        self.assertIn(self.cuisine, self.restaurant.cuisines.all())

    def test_menu_item_creation(self):
        menu = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Dosa",
            description="Hot and Crispy Dosa ",
            price=Decimal("80.00"),
        )
        self.assertEqual(menu.name, "Dosa")
        self.assertEqual(menu.restaurant, self.restaurant)

    def test_menu_item_gets_deleted_on_cascade(self):
        menu = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Dosa",
            description="Hot and Crisp Dosa",
            price=Decimal("80.00"),
        )
        self.restaurant.delete()
        self.assertEqual(MenuItem.objects.count(), 0)
