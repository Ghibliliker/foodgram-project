from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe, Shopping,
                     Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
