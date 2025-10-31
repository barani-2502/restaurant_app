from django.contrib import admin
from .models import Restaurant, MenuItem, MenuItemPhoto, RestaurantPhoto, Cuisine, Bookmark

class MenuItemPhotoInline(admin.TabularInline):
    model = MenuItemPhoto
    extra = 0 

class RestaurantPhotoInline(admin.TabularInline):
    model = RestaurantPhoto
    extra = 0

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

@admin.register(Bookmark)
class BookmarksAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user')
    search_fields = ('restaurant__name', 'user__username')
