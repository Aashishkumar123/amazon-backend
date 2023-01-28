from rest_framework.views import APIView
from rest_framework.response import Response
from amazon_backend_api.api.serializers import AmazonuserSerializer, AmazonuserAddressSerializer
from amazon_backend_api.models import Amazonuser, UserAddress
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from amazon_backend_api.api.helpers import (
    get_tokens_for_user,
    get_user_from_token
)
from rest_framework.permissions import IsAuthenticated


class RegisterAPIView(APIView):
    def post(self,request):
        data = request.data
        serializer = AmazonuserSerializer(data=data)
        if serializer.is_valid():
            Amazonuser.objects.create(
                full_name = serializer.validated_data['full_name'],
                email = serializer.validated_data['email'],
                password = make_password(serializer.validated_data['password'])
            )
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'created',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST) 


class SigninAPIView(APIView):
    def post(self,request):
        if 'email' not in request.data or 'password' not in request.data:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : 'email or password should not empty'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        password = request.data['password']

        user = authenticate(request,email=email,password=password)
        if user is not None:
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'success',
                'data' : get_tokens_for_user(Amazonuser.objects.get(email=email))
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : 'email or password is wrong'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class UserAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = get_user_from_token(request)
        address = UserAddress.objects.filter(user=user)
        serialize_address = AmazonuserAddressSerializer(address,many=True)
        response = {
            "status" : status.HTTP_200_OK,
            "message" : 'OK',
            "data" : serialize_address.data
        }
        return Response(response,status=status.HTTP_200_OK)
