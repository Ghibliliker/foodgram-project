from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    username = models.CharField(
        max_length=100, unique=True,
        blank=True, verbose_name='Username пользователя')
    email = models.EmailField(
        blank=True, unique=True, verbose_name='mail пользователя')
    first_name = models.CharField(
        max_length=100, verbose_name='Имя пользователя')
    last_name = models.CharField(
        max_length=100, verbose_name='Фамилия пользователя')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower', verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор на которого подписан пользователь'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='user_following_unique'
            ),
            models.CheckConstraint(
                check=~Q(user=F('following')),
                name='not_yourself_following'
            )
        ]
