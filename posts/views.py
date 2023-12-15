from datetime import datetime

from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .services_post import PostService


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@api_view(["POST"])
def like_post(request, id):
    try:
        user = request.user
        post = PostService.get_post_by_id_or_404(id)
        result, status = PostService.like_post(post, user)
        return Response(result, status=status)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unlike_post(request, id):
    try:
        user = request.user
        post = PostService.get_post_by_id_or_404(id)
        result, status = PostService.unlike_post(post, user)
        return Response(result, status=status)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class AnalyticView(APIView):

    def get(self, request):
        date_from_str = request.query_params.get('date_from', '')
        date_to_str = request.query_params.get('date_to', '')

        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # Get analytics data for post likes within the specified date range
        likes_data = Post.objects.filter(
            created_at__date__range=[date_from, date_to]
        ).values('created_at__date').annotate(likes=Sum('likes'))

        return Response(likes_data)
