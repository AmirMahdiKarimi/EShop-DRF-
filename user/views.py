from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth.signals import user_logged_out
from rest_framework.generics import get_object_or_404, CreateAPIView, UpdateAPIView, RetrieveAPIView
from knox.auth import TokenAuthentication

from .models import CustomeAuthToken
from .utils import get_user_agent
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChangePassSerializer, \
     CustomeAuthTokenSerializer, SetProfileSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        user_agent = get_user_agent(request)
        token = CustomeAuthToken.objects.create(user, user_agent=user_agent)
        return Response(
            {'token': token[1],
            },status=200
        )
    

class LoginApiView(APIView):
    def post(self, request):
        user_serializer = LoginSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.validated_data

            user_agent = get_user_agent(request)
            token = CustomeAuthToken.objects.create(user, user_agent=user_agent)

            return Response(
                {'token': token[1],
                },status=200
            )
        return Response(
            {'message': user_serializer.errors},
            status=400
        )
    

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(data={'message': 'successful logout!'}, status=200)
    

class ChangePassAPIView(UpdateAPIView):
    serializer_class = ChangePassSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('old_pass')
        user = self.get_object()

        if check_password(password, user.password):
            tokens = CustomeAuthToken.objects.filter(user=user)
            tokens.delete()
            serializer.update(user, serializer.validated_data)
            user_agent = get_user_agent(request)
            token = CustomeAuthToken.objects.create(user, user_agent=user_agent)
            return Response({'token': token[1]}, status=200)
        else:
            return Response({"message": "Wrong password!"}, status=403)


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
                

class SetProfileAPIView(UpdateAPIView):
    serializer_class = SetProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

