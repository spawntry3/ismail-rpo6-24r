from django.contrib import admin
from .models import Category, City, Ad, Favorite, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  
    prepopulated_fields = {'slug': ('name',)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'city', 'price', 'is_moderated', 'is_top', 'created_at')
    list_filter = ('is_moderated', 'is_top', 'category', 'city')
    list_editable = ('is_moderated', 'is_top')
    search_fields = ('title', 'author__username')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'comment')


