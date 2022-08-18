from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg

from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from reviews.models import Category, Genre, Review, Title

from .mixins import MyMixinViewSet
from .permissions import (AdminOnly, AdminOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly, IsOwnerOrReadOnly,
                          ModeratorOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MeSerializer, ReviewSerializer,
                          SignUpSerializer, TitleGetSerializer,
                          TitlePostSerializer, TokenSerializer,
                          UserByAdminSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""

    queryset = User.objects.all()
    serializer_class = UserByAdminSerializer
    permission_classes = (AdminOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'


class SignUp(APIView):
    """New User Registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        email = serializer.data['email']
        if (User.objects.filter(email=email).exists()
                or User.objects.filter(username=username).exists()):
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user, create = User.objects.get_or_create(email=email,
                                                  username=username)
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class PullToken(APIView):
    """Getting a JWT token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            response = {'token': str(token.access_token)}
            return Response(response, status=status.HTTP_200_OK)

        response = {username: 'Ошибка! Некорректный токен'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MyAPIView(APIView):
    """View for User model - author."""

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = MeSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = MeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model."""

    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model."""

    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly | ModeratorOnly | AdminOnly, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class TitleFilter(FilterSet):
    """Filter for Title model."""

    category = CharFilter(field_name='category__slug', lookup_expr='iexact',)
    genre = CharFilter(field_name='genre__slug', lookup_expr='iexact',)
    name = CharFilter(field_name='name', lookup_expr='icontains',)

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for Title model."""

    queryset = Title.objects.order_by('name').annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitlePostSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitlePostSerializer
        return TitleGetSerializer


class CategoryViewSet(MyMixinViewSet):
    """ViewSet for Category model"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(MyMixinViewSet):
    """ViewSet for Genre model"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
