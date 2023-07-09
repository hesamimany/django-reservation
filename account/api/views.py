from django.contrib.auth import authenticate, get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from account.api.serializer import UserSerializer, UserCreateSerializer
from account.models import CustomUser


class UserAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create a session
            request.session['user_id'] = user.id

            # Set a cookie
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie('user_id', user.id)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk, end="\n\n\n\n\n\n\n\n")
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            return CustomUser.objects.get(pk=int(pk))
        except CustomUser.DoesNotExist:
            raise Http404


class LoginAPIView(APIView):

    def post(self, request):
        request.session.pop(f'password_attempt:{request.META.get("REMOTE_ADDR")}', None)

        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        # print(password, end="\n")
        # print(get_user_model().objects.all().get(phone_number=phone_number).password)
        user = authenticate(request=request, phone_number=phone_number, password=password)
        print(user, end="\n\n\n\n\n")
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'User not found'}, status=401)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.my_user
        Token.objects.filter(user=user).delete()
        return Response({'success': 'Logged out successfully'})


class SignupAPIView(APIView):
    def post(self, request):

        # if phone_number not in CustomUser.objects.all().filter(phone_number=phone_number):
        #     return Response({'error': 'User already exists'}, status=401)
        # else:
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.create(serializer.validated_data)
            print(user, end="\n\n\n\n")
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response({'message': "else of post create"}, status=401)
