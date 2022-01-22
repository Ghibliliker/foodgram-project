from django.db import models

from .validators import number_validator
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя тега')
    color = models.CharField(max_length=200, verbose_name='Цвет тега')
    slug = models.SlugField(unique=True, verbose_name='Slug тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe', verbose_name='Ингредиенты рецепта'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор'
    )
    image = models.ImageField(upload_to='api/', verbose_name='Картинка')
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        validators=[number_validator], verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.IntegerField(
        verbose_name='Количество ингредиента в рецепте')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe', verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_favorite_unique'
            )
        ]


class Shopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping', verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_shopping_unique'
            )
        ]
