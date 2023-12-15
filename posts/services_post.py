from django.http import Http404

from rest_framework import status
from rest_framework.generics import get_object_or_404

from .utils import update_last_request
from .models import Post

from loguru import logger


class PostService:

    @staticmethod
    def get_post_by_id_or_404(post_id):
        """Get a post by its ID or raise Http404 if not found"""
        try:
            post = get_object_or_404(Post, id=post_id)
            logger.info(f"Retrieved post with ID {post_id}")
            return post
        except Http404:
            logger.warning(f"Post with ID {post_id} not found")
            raise

    @staticmethod
    def like_post(post, user):
        """Like a post and return a response with updated likes count if successful"""
        try:
            post.like_post(user)
            likes = post.likes
            update_last_request(user)
            logger.info(f"Post liked successfully. Post ID: {post.id}, User ID: {user.id}")
            return {'message': 'Post liked successfully', 'likes': likes}, status.HTTP_200_OK
        except Post.DoesNotExist:
            logger.warning(f"Like failed. Post not found. Post ID: {post.id}, User ID: {user.id}")
            return {'error': 'Post not found'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def unlike_post(post, user):
        """Unlike a post and return a response with updated likes count if successful"""
        try:
            post.unlike_post(user)
            likes = post.likes
            update_last_request(user)
            logger.info(f"Post unliked successfully. Post ID: {post.id}, User ID: {user.id}")
            return {'message': 'Post unliked successfully', 'likes': likes}, status.HTTP_200_OK
        except Post.DoesNotExist:
            logger.warning(f"Unlike failed. Post not found. Post ID: {post.id}, User ID: {user.id}")
            return {'error': 'Post not found'}, status.HTTP_404_NOT_FOUND
