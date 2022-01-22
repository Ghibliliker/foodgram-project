from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.pagination import CustomPageNumberPagination
from .models import Subscribe, User
from .serializers import SubscribeSerializer, SubscribeUserSerializer


class APIFollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = self.request.user
        following = get_object_or_404(User, id=self.kwargs['pk'])
        data = {'user': user.id, 'following': following.id}
        serializer = SubscribeSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, following=following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = self.request.user
        following = get_object_or_404(User, id=self.kwargs['pk'])
        data = {'user': user.id, 'following': following.id}
        serializer = SubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIFollowList(ListAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeUserSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
