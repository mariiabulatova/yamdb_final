from django.urls import include, path

from rest_framework import routers

from . import views


router_v1 = routers.DefaultRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')
router_v1.register(r'titles', views.TitleViewSet, basename='titles')
router_v1.register(r'genres', views.GenreViewSet, basename='genres')
router_v1.register(r'categories', views.CategoryViewSet, basename='categories')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/auth/signup/', views.SignUp.as_view()),
    path('v1/auth/token/', views.PullToken.as_view()),
    path('v1/users/me/', views.MyAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
