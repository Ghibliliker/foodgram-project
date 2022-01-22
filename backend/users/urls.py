from django.urls import include, path

from .views import APIFollow, APIFollowList

urlpatterns = [
    path(
        'users/subscriptions/',
        APIFollowList.as_view(),
        name='subscriptions-list'),
    path(
        'users/<int:pk>/subscribe/',
        APIFollow.as_view(),
        name='subscribe-detail'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
