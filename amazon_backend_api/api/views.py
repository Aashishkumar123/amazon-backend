from rest_framework.views import APIView
from rest_framework.response import Response
from amazon_backend_api.api.serializers import (
    AmazonuserSerializer,
    AmazonuserAddressSerializer
)
from amazon_backend_api.models import (
    Amazonuser,
    UserAddress
)
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from amazon_backend_api.api.helpers import (
    get_tokens_for_user,
    get_user_from_token
)
from rest_framework.permissions import IsAuthenticated


'''
This api used for registeration...
'''
class RegisterAPIView(APIView):

    def post(self,request):
        data = request.data
        serializer = AmazonuserSerializer(data=data)
        if serializer.is_valid():
            amz_user = Amazonuser.objects.create(
                full_name = serializer.validated_data['full_name'],
                email = serializer.validated_data['email'],
                password = make_password(serializer.validated_data['password'])
            )
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'created',
                'data' : get_tokens_for_user(Amazonuser.objects.get(email=amz_user.email))
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST) 


'''
This api is used for sign in.....
'''
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


'''
This api is used to get , update , delete , create the user address.....
'''
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

    def post(self,request):
        data = request.data
        user = get_user_from_token(request)
        serialize_address = AmazonuserAddressSerializer(data=data)
        if serialize_address.is_valid():
            created_adrs = serialize_address.save(user=user)
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'address created',
                'data' : AmazonuserAddressSerializer(UserAddress.objects.get(id=created_adrs.id)).data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : serialize_address.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        if 'id' not in request.data:
            response = {
                'status' : '400',
                'message' : 'bad request',
                'data' : {
                'id' : [
                        "This field is required."
                    ]
                }
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        try:
            adrs_id = UserAddress.objects.get(id=data['id'])
        except UserAddress.DoesNotExist:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'Id does not exist.'
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        serialize_address = AmazonuserAddressSerializer(adrs_id,data=data)
        if serialize_address.is_valid():
            serialize_address.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'updated'
            }
            return Response(response,status=status.HTTP_200_OK)
        response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : serialize_address.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        if 'id' not in request.data or not request.data['id']:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : {
                'id' : [
                        "This field is required."
                    ]
            }
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data['id']

        try:
            UserAddress.objects.get(id=address_id).delete()
        except UserAddress.DoesNotExist:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'Id does not exist.'
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        response = {
            'status' : status.HTTP_204_NO_CONTENT,
            'message' : 'Address deleted.'
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)


'''
This api will set a default address....
'''
class SetdefaultAddressAPIView(APIView):

    def post(self,request,id):
        user = get_user_from_token(request)
        UserAddress.objects.filter(user=user).update(default=False)
        
        try:
            update_default_adrs = UserAddress.objects.get(id=id)
            update_default_adrs.default = True
            update_default_adrs.save()
        except UserAddress.DoesNotExist:
            response = {
            'status' : status.HTTP_404_NOT_FOUND,
            'message' : 'ID not found'
        }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success'
        }
        return Response(response,status=status.HTTP_200_OK)
