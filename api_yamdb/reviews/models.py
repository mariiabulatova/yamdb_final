from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def current_year():
    return datetime.now().year


class User(AbstractUser):
    """User model."""

    ROLES = [
        ('user', 'Аутентифицированный юзер'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    ]

    email = models.EmailField('email адрес', unique=True)
    bio = models.TextField('о себе', blank=True)
    role = models.CharField(
        'статус',
        max_length=78,
        choices=ROLES,
        default='user',
        blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)

    class Meta:
        """Additionally for User model."""
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Return user username."""
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Category(models.Model):
    """Category model."""

    name = models.CharField('name', max_length=78)
    slug = models.SlugField('slug', unique=True, max_length=78)

    class Meta:
        """Additionally for Category model."""

        ordering = ('slug',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return category slug."""
        return self.slug


class Genre(models.Model):
    """Genre model."""

    name = models.CharField('name', max_length=78)
    slug = models.SlugField('slug', unique=True, max_length=78)

    class Meta:
        """Additionally for Genre model."""

        ordering = ('slug',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        """Return genre slug."""
        return self.slug


class Title(models.Model):
    """Title model."""

    name = models.CharField('name', max_length=78,)
    year = models.PositiveSmallIntegerField(
        'release year',
        validators=[
            MaxValueValidator(
                current_year,
                'The time machine has not been invented yet.'
            ),
            MinValueValidator(
                1895,
                'Start at 1895 - year of invention of cinema.'
            ),
        ],
    )
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='category',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='genre',
    )
    description = models.TextField('description', blank=True,)

    class Meta:
        """Additionally for Title model."""

        ordering = ('name',)
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        indexes = [
            models.Index(fields=['year', ]),
        ]

    def __str__(self):
        """Return title name."""
        return self.name


class Review(models.Model):
    """Review model."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews'
                               )
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews'
                              )
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')
        ]
    )

    class Meta:
        """Additionally for Review model."""

        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_review')
        ]

    def __str__(self):
        """Return review text."""
        return self.text[:20]


class Comment(models.Model):
    """Comment model."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        """Additionally for Comment model."""
        ordering = ('-pub_date',)

    def __str__(self):
        """Return comment text."""
        return self.text[:25]
