import django_filters
from .models import Restaurant
from django import forms

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
    open_status = django_filters.BooleanFilter(
        field_name='open_status',
        widget=forms.Select(
            choices=[
                ('', 'Open/Closed'),
                ('true', 'Open'),
                ('false', 'Closed'),
            ]
        )
    )

    sort = django_filters.ChoiceFilter(
        choices=[
                ('', 'Sort By'),
                ('cost_asc', 'Cost ↑'),
                ('cost_desc', 'Cost ↓'),
                ('rating_asc', 'Rating ↑'),
                ('rating_desc', 'Rating ↓'),
            ],
            label='Sort By',
            method = 'sort_by',
            empty_label = None
    )

    def sort_by(self, queryset, name, value):
        sort_options = {
            'cost_asc': 'cost_for_two',
            'cost_desc': '-cost_for_two',
            'rating_asc': 'average_rating',
            'rating_desc': '-average_rating',
        }

        order_by_field = sort_options.get(value)
        if order_by_field:
            queryset = queryset.order_by(order_by_field)

        return queryset

    class Meta:
        model = Restaurant
        fields = ['name', 'city', 'cuisines', 'food_type', 'open_status', 'sort']

