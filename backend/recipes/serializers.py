from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe, Shopping,
                     Tag)
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags',
            'image', 'name',
            'text', 'cooking_time', 'author')
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Ингредиент должен быть больше нуля!'
                })
        return data

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            id = ingredient['id']
            current_ingredient = get_object_or_404(Ingredient, pk=id.id)
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=amount)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags_list = validated_data.pop('tags', instance.tags)
        ingredients_list = validated_data.pop(
            'ingredients', instance.ingredients)
        instance.tags.clear()
        self.create_tags(tags_list, instance)
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(ingredients_list, instance)
        instance.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(
            instance, context=context
        ).data


class IngredientListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientListSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Shopping.objects.filter(user=request.user, recipe=obj).exists()


class RecipeFavoriteShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeFavoriteShoppingSerializer(
            instance.recipe, context=context
        ).data


class ShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shopping
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeFavoriteShoppingSerializer(
            instance.recipe, context=context
        ).data
