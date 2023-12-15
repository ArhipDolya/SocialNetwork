import datetime
import jwt

from loguru import logger

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .config import SECRET_JWT
from .serializers import UserSerializer
from .utils import generate_token, update_last_request


logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


class AuthService:
    """
    Service class for user authentication-related functionality
    """

    @staticmethod
    def register_user(serializer_data):
        serializer = UserSerializer(data=serializer_data)

        if serializer.is_valid():
            user = serializer.save()

            # Log a successful registration
            logger.info(f"User registered successfully: {user.username}")

            return {'message': 'User registered successfully'}, 201

        logger.error(f"Registration failed: {serializer.errors}")
        return serializer.errors, 400

    @staticmethod
    def login_user(email, password):
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        access_token = generate_token(user.id, expires_delta=datetime.timedelta(minutes=15))
        refresh_token = generate_token(user.id, expires_delta=datetime.timedelta(days=7))

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        AuthService.set_tokens_in_response(response_data)

        user.last_login = datetime.datetime.utcnow()
        user.save()
        update_last_request(user)

        return response_data, 200

    @staticmethod
    def get_user_data(token):
        """Retrieves user data based on the provided token"""

        if not token:
            logger.error("Get user data failed: Unauthenticated request")
            return Response({'error': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.error("Get user data failed: Expired signature")
            return Response({'error': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=payload['id']).first()

        update_last_request(user)

        logger.info(f"User data retrieved successfully for user {user.username}")
        return user

    @staticmethod
    def refresh_token(refresh_token):
        if not refresh_token:
            logger.error("Refresh token failed: No refresh token provided")
            raise AuthenticationFailed('No refresh token provided!')

        try:
            payload = jwt.decode(refresh_token, SECRET_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.error("Refresh token failed: Expired signature")
            raise AuthenticationFailed('Expired refresh token!')

        user = User.objects.filter(id=payload['id']).first()

        if not user:
            logger.error("Refresh token failed: User not found")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        access_token = generate_token(user.id, expires_delta=datetime.timedelta(minutes=15))

        logger.info(f"Refresh token successful for user {user.username}")
        return {
            'access_token': access_token,
            'expires_in': 15 * 60,  # seconds
        }

    @staticmethod
    def get_user_activity(access_token):
        """Retrieves user activity information based on the provided access token"""

        if not access_token:
            logger.error("Get user activity failed: Unauthenticated request")
            return Response({'error': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(access_token, SECRET_JWT, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.error("Get user activity failed: Expired signature")
            return Response({'error': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('id')
        user = User.objects.filter(id=user_id).first()

        if not user:
            logger.error("Get user activity failed: User not found")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"User activity retrieved successfully for user {user.username}")
        return {
            'last_login': user.last_login,
            'last_request': user.last_request,
        }

    @staticmethod
    def set_tokens_in_response(response_data):
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token,
                            expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=15), httponly=True)
        response.set_cookie('refresh_token', refresh_token,
                            expires=datetime.datetime.utcnow() + datetime.timedelta(days=7), httponly=True)

        return response
