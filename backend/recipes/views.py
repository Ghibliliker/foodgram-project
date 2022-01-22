from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientRecipe, Recipe, Shopping,
                     Tag)
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingSerializer, TagSerializer)
from .utils import favorite_shopping_recipe


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        detail=True,
        permission_classes=(IsAuthenticated,),
        methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        return favorite_shopping_recipe(
            self, request, pk, FavoriteSerializer, Favorite)

    @action(
        detail=True,
        permission_classes=(IsAuthenticated,),
        methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        return favorite_shopping_recipe(
            self, request, pk, ShoppingSerializer, Shopping)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        data = IngredientRecipe.objects.filter(
            recipe__shopping__user=request.user.id).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(summ=Sum('amount'))
        text = []
        for ingredient in data:
            text.append(
                f'Имя: {ingredient["ingredient__name"]}'
                + f'({ingredient["ingredient__measurement_unit"]}) -'
                + f'{ingredient["summ"]}')
        response = HttpResponse('\n'.join(text), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="Покупки.txt"'
        return response
