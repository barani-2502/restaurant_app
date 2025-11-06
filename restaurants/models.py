from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User

class Cuisine(models.Model):
    """
    Represents the type of cuisine(eg., Chinese, Italian, etc) 
    which can be associated with restaurants
    """
    name = models.CharField(
        max_length=50,
        help_text="Enter the name of cuisine"
    )
    
    description = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="Optional description of the cuisine"
    )

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    """
    Represents a restaurant with details, cuisine,
    food type, cost, open status and spotlight status.
    """
    class FoodType(models.TextChoices):
        VEG = 'veg', 'Vegetarian'
        NON_VEG = 'non_veg', 'Non-Vegetarian'
        VEGAN = 'vegan', 'Vegan'

    name = models.CharField(
        max_length=50,
        help_text="Name of the restaurant"
    )

    address = models.CharField(
        max_length=200,
        help_text="Address of the restaurant"
    )

    city = models.CharField(
        max_length=30,
        help_text="City where the restaurant is located",
    )

    cost_for_two = models.IntegerField(
        help_text="Average cost for two people"
    )

    food_type = models.CharField(
        max_length=15,
        choices=FoodType.choices,
        default=FoodType.NON_VEG,
        help_text="Type of food: Veg / Non-veg / Vegan"
    )

    open_status = models.BooleanField(
        default=True,
        help_text="Is the restaurant currently open?",
    )

    cuisines = models.ManyToManyField(
        Cuisine,
        related_name='restaurants',
        help_text="Cuisines served by the restaurant"
    )

    spotlight = models.BooleanField(
        default=False,
        help_text="Set True to display the restaurant on homepage"
    )

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    """
    Represents a food item from meny of a restaurant.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        on_delete=models.CASCADE,
        help_text="The restaurant that offers this menu item"
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the dish"
    )
    description = models.CharField(
        max_length=200,
        help_text="Description of the dish"
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price of the dish",
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
    )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name="price_non_negative")
        ]

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class RestaurantPhoto(models.Model):
    """
    Stores photos of a restaurant.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='restaurant_photos',
        on_delete=models.CASCADE,
        help_text="The name of the restaurant of the given photo"
    )
    image = models.ImageField(
        upload_to='restaurant_photos/',
        blank=True,
        null=True,
        help_text="Images of the restaurant"
    )

    def __str__(self):
        return f"Photo of {self.restaurant.name}"

class MenuItemPhoto(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        related_name='menu_item_photos',
        on_delete=models.CASCADE,
        help_text="Represents the menu item of the given image"
    )

    image = models.ImageField(
        upload_to='menu_items/',
        blank=True,
        null=True,
        help_text="Image of the menu item"
    )

    def __str__(self):
        return f"Photo of {self.menu_item.name}"
    
class Bookmark(models.Model):
    """
    Stores the restaurants bookmarked by a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookmarked_by_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.restaurant.name}"

class Visit(models.Model):
    """
    Represents a record of a user visiting a restaurant.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='visited_by_user')
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')
        ordering = ['-visited_at']

    def __str__(self):
        return f'{self.user.username} visited {self.restaurant.name}'
