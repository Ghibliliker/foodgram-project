from rest_framework import status
from rest_framework.response import Response


def favorite_shopping_recipe(self, request, pk, serializer, model):
    user = request.user.id
    id = self.kwargs['pk']
    if request.method == 'POST':
        data = {'user': user, 'recipe': id}
        serializer = serializer(
            data=data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    model.objects.filter(user=user, recipe=id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
