import django_filters
from .models import Restaurant

class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Name')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains', label='City')
    cuisines = django_filters.CharFilter(field_name='cuisines__name', lookup_expr='icontains', label='Cuisine')
    food_type = django_filters.ChoiceFilter(
        choices=[('', 'Select Food Type')] + Restaurant.FoodType.choices, 
        field_name='food_type',
        label='',
        empty_label=None,
    )
    open_status = django_filters.BooleanFilter(field_name='open_status')

    class Meta:
        model = Restaurant
        fields = ['name', 'city', 'cuisines', 'food_type', 'open_status']
        