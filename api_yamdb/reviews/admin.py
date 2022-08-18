from django.contrib import admin

from .models import Category, Genre, Title, User

EMPTY_VALUE_DISPLAY = '-пусто-'

admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Registering model Category in the admin panel."""
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Registering model Genre in the admin panel."""
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Registering model Title in the admin panel."""
    list_display = ('pk', 'name', 'year', 'category',)
    search_fields = ('name',)
    list_filter = ('name',)
