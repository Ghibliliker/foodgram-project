from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Subscribe, User
from recipes.models import Recipe


class CustomUserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'id', 'password', 'email', 'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'id',
            'email', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user, following=obj
        ).exists()


class RecipeFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscribeUserSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'recipes',
            'is_subscribed', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user, following=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        context = {'request': request}
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            queryset = obj.recipes.all()[:int(recipes_limit)]
        else:
            queryset = obj.recipes.all()
        return RecipeFollowingSerializer(
            queryset, many=True, context=context
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'following')
        model = Subscribe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SubscribeUserSerializer(
            instance.following, context=context
        ).data
