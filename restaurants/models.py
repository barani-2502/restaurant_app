from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    veg = 'veg'
    non_veg = 'non_veg'
    vegan = 'vegan'

    FOOD_TYPE_CHOICES = [
        (veg, 'Vegetarian'),
        (non_veg, 'Non-Vegetarian'),
        (vegan, 'Vegan'),
    ]

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    cost_for_two = models.IntegerField()
    food_type = models.CharField(
        max_length=15,
        choices=FOOD_TYPE_CHOICES,
        default=non_veg,
    )
    open_status = models.BooleanField(default=True)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')
    spotlight = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items' , on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_photos' , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)