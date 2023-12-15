import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer
from .exceptions import UnauthenticatedException
from .services_auth import AuthService


class RegistrationView(APIView):

    def post(self, request):
        response_data, status_code = AuthService.register_user(request.data)
        return Response(response_data, status_code)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            response_data, status_code = AuthService.login_user(email, password)
            return AuthService.set_tokens_in_response(response_data)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=e.status_code)


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('access_token')

        try:
            user = AuthService.get_user_data(token)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UnauthenticatedException as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.data = {'message': 'logged out'}

        return response


class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('No refresh token provided!')

        try:
            result = AuthService.refresh_token(refresh_token)
            response = Response(result, status=status.HTTP_200_OK)
            response.set_cookie('access_token', result['access_token'], expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=15), httponly=True)
            return response
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=e.status_code)


class UserActivityView(APIView):

    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        try:
            result = AuthService.get_user_activity(access_token)
            return Response(result, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=e.status_code)

