from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet,
                    UserViewSet)

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('users', UserViewSet, basename='users')
router.register('groups', GroupViewSet, basename='groups')
router.register('posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comments'
                )
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
