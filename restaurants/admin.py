from django.contrib import admin
from .models import Restaurant, MenuItem, MenuItemPhoto, RestaurantPhoto, Cuisine

class MenuItemPhotoInline(admin.TabularInline):
    model = MenuItemPhoto
    extra = 1 

class RestaurantPhotoInline(admin.TabularInline):
    model = RestaurantPhoto
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'open_status', 'spotlight')
    search_fields = ('name', 'address', 'city')
    ordering = ('name',)
    inlines = [RestaurantPhotoInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_editable = ('price',) 
    search_fields = ('name',)
    list_filter = ('restaurant',)
    ordering = ('restaurant', 'name')
    inlines = [MenuItemPhotoInline]

@admin.register(MenuItemPhoto)
class MenuItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'image')

@admin.register(RestaurantPhoto)
class RestaurantPhotoAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

