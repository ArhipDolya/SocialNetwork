from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', views.AnalyticView.as_view()),
    path('posts/like/<int:id>/', views.like_post),
    path('posts/unlike/<int:id>/', views.unlike_post),
]