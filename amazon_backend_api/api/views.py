from rest_framework.views import APIView
from rest_framework.response import Response
from amazon_backend_api.api.serializers import (
    AmazonuserSerializer,
    AmazonuserAddressSerializer,
    BrandSerializer,
    ProductDetailsSerializer,
    CartSerializer,
    AmazonuserLoginSerializer
)
from amazon_backend_api.models import (
    Amazonuser,
    UserAddress,
    Brand,
    Product,
    ProductDetail,
    Subcategory,
    Cart
)
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from amazon_backend_api.api.helpers import (
    get_tokens_for_user,
    get_user_from_token,
    get_access_token_from_refresh_token
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


class SigninAPIView(APIView):
    """""This api is handling login"""""

    def post(self,request):
        """Handle post request"""

        login_serializer = AmazonuserLoginSerializer(data=request.data)

        """it will check data validation"""
        if login_serializer.is_valid():

            """get email and password"""
            email = login_serializer.validated_data['email']
            password = login_serializer.validated_data['password']

            """it will check the credentials is valid or not"""
            user = authenticate(request,email=email,password=password)

            """it will return access token if credentials are ok"""
            if user is not None:
                
                """return the user information and tokens"""
                res_data = get_tokens_for_user(
                    Amazonuser.objects.get(email=email)
                    )
                response = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'success',
                    'data' : res_data
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                """otherwise return this response"""
                response = {
                    'status' : status.HTTP_401_UNAUTHORIZED,
                    'message' : 'Invalid Email or Password'
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)

        """if validation failed it return this"""
        response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : login_serializer.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


class RegenerateAccessToken(APIView):

    def post(self,request):
        data = request.data
        if 'refresh_token' not in data and 'grant_type' not in data:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : {
                'refresh_token' : [
                    'refresh_token is required'
                ],
                'grant_type' : [
                    'grant_type is required'
                ]
            }
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        if 'refresh_token' not in data:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : {
                'refresh_token' : [
                    'refresh_token is required'
                ]
            }
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        if 'grant_type' not in data:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : {
                'grant_type' : [
                    'grant_type is required'
                ]
            }
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        data = get_access_token_from_refresh_token(request)
        
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success',
            'data' : data if data else []
            }
        return Response(response,status=status.HTTP_200_OK)


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
        user = get_user_from_token(request)
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
            user_address = UserAddress.objects.filter(user=user)
            adrs_id = user_address.get(id=data['id'])
        except UserAddress.DoesNotExist:
            response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'Id does not exist.'
        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        serialize_address = AmazonuserAddressSerializer(adrs_id,data=data)
        if serialize_address.is_valid():
            updated_adrs = serialize_address.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'address updated',
                'data' : AmazonuserAddressSerializer(UserAddress.objects.get(id=updated_adrs.id)).data
            }
            return Response(response,status=status.HTTP_200_OK)
        response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : serialize_address.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user = get_user_from_token(request)
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
            UserAddress.objects.filter(user=user).get(id=address_id).delete()
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

    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        user = get_user_from_token(request)
        df_adrs =  UserAddress.objects.filter(user=user)
        df_adrs.filter(default=True).update(default=False)
        
        try:
            update_default_adrs = df_adrs.get(id=id)
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


'''
This api will GET and Save the new brands
'''
class BrandAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands = Brand.objects.all()
        brand_serializer = BrandSerializer(brands, many=True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success',
            'data' : brand_serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        brand_serializer = BrandSerializer(data=data)
        if brand_serializer.is_valid():
            brand = brand_serializer.save()
            response = {
            'status' : status.HTTP_201_CREATED,
            'message' : 'brand created',
            'data' : BrandSerializer(Brand.objects.get(id=brand.id)).data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'bad request',
            'data' : brand_serializer.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


'''
This api return all the products on the base of its subcategory
'''
class ProductsAPIView(APIView):

    def get(self,request,subcategory1,subcategory2=None):
        if subcategory2:
             products = Product.objects.filter(
                    subcategory1=Subcategory.objects.filter(name__iexact=subcategory1).first(),
                    subcategory2=Subcategory.objects.filter(name__iexact=subcategory2).first()
                    ).first()
        else:
            products = Product.objects.filter(
                    subcategory1=Subcategory.objects.filter(name__iexact=subcategory1).first()
                    ).first()

        allproducts = ProductDetail.objects.filter(product=products)
        allproducts_serializer = ProductDetailsSerializer(allproducts,many=True)

        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success',
            'data' : allproducts_serializer.data
            }
        return Response(response,status=status.HTTP_200_OK)


'''
This api return single product details
'''
class ProductDetailsAPIView(APIView):

    def get(self,request,product_id,product_detail_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'product not found.'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        product_details = ProductDetail.objects.filter(product=product)

        if not product_details.filter(id=product_detail_id):
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'product not found.',
                'data' : []
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        product_details_serializer = ProductDetailsSerializer(product_details,many=True)

        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success',
            'active_product_detail_id' : product_detail_id,
            'data' : product_details_serializer.data
            }
        return Response(response,status=status.HTTP_200_OK)


'''
cart api that will get all the products of an user
cart api that will add product to the cart of an user
cart api that will update the product quantity of an user
cart api that will remove the product from cart of an user
'''
class CartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    '''
    Return all the products from cart for particular user
    '''
    def get(self,request):
        user = get_user_from_token(request)
        cart = Cart.objects.filter(user=user)
        cart_serializer = CartSerializer(cart,many=True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'success',
            'data' : cart_serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
    '''
    Add the product to cart for a particular user
    '''
    def post(self,request):
        user = get_user_from_token(request)
        data = request.data
        
        '''
        This will response 404 if product_id not in request data
        '''
        if 'product_id' not in data:
            response = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'bad request',
                    'data' : {
                        'product_id' : 'Product id should not empty'
                    }
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        This will response 404 status code if get wrong product id
        '''
        try:
            product_id = ProductDetail.objects.get(id=request.data['product_id'])
        except ProductDetail.DoesNotExist:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : {
                    'product_id' : 'Invalid product id'
                }
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        '''
        This will check product already in cart then will response 404 status code
        '''
        if Cart.objects.filter(user=user,product=data['product_id']).exists():
                response = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'bad request',
                    'data' : {
                        'product' : 'Product already in cart'
                    }
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        If everything fine this will add product to cart
        '''
        cart_serializer = CartSerializer(data=data)
        if cart_serializer.is_valid():
            cart_serializer.save(user=user,product=product_id)
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'proudct added to cart'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        else return 404 status code
        '''
        response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : cart_serializer.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    '''
    This will update the product quantity of a particular user
    '''
    def patch(self,request):
        data = request.data
        user = get_user_from_token(request)
        
        '''
        This will check request data is having id or not
        '''
        if 'id' not in data:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : {
                    'id' : [
                        'id is required'
                    ]
                }
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        This will check the cart id is belong the authenticated user
        '''
        if not Cart.objects.filter(user=user,id=data['id']).exists():
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : {
                    'id' : [
                        'invalid cart id'
                    ]
                }
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        This will check the validation and update the product quantity
        '''
        cart_serializer = CartSerializer(instance=Cart.objects.get(id=data['id']),data=data,partial=True)
        if cart_serializer.is_valid():
            cart_serializer.save()
            response = {
                'status' : status.HTTP_202_ACCEPTED,
                'message' : 'quantity updated',
                'data' : CartSerializer(Cart.objects.get(id=cart_serializer.data['id'])).data
            }
            return Response(response,status=status.HTTP_202_ACCEPTED)
        
        '''
        otherwise it raise the validation
        '''
        response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'bad request',
                'data' : cart_serializer.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    '''
    This will remove product from cart of a particular user 
    '''
    def delete(self,request):
        data = request.data
        user = get_user_from_token(request)
        '''
        This will response 404 if product_id not in request data
        '''
        if 'product_id' not in data:
            response = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'bad request',
                    'data' : {
                        'product_id' : 'Product id should not empty'
                    }
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        '''
        This will check product avaliable in cart to delete
        '''
        if Cart.objects.filter(user=user,product=data['product_id']).exists():
            Cart.objects.get(product=data['product_id']).delete()
            response = {
                    'status' : status.HTTP_204_NO_CONTENT,
                    'message' : 'product remove from cart',
                }
            return Response(response,status=status.HTTP_204_NO_CONTENT)
        
        '''
        other response inavlid product id
        '''
        response = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'bad request',
                    'data' : {
                        'product_id' : 'Invalid product id'
                    }
                }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
