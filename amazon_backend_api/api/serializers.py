from rest_framework import serializers
from amazon_backend_api.models import (
    Amazonuser,
    UserAddress,
    Brand,
    Product,
    ProductDetail,
    Size,
    Cart
)
from rest_framework.serializers import ALL_FIELDS
from django.contrib.auth.hashers import make_password


class AmazonuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amazonuser
        fields = ['email','full_name','password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(AmazonuserSerializer, self).create(validated_data)


class AmazonuserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = Amazonuser
        fields = ['email','password']


class AmazonuserAddressSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data):
        return UserAddress.objects.create(**validated_data)

    class Meta:
        model = UserAddress
        fields = ALL_FIELDS


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ALL_FIELDS


class ProductSerializer(serializers.ModelSerializer):

    brand = serializers.CharField(source="brand.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    subcategory1 = serializers.CharField(source="subcategory1.name", read_only=True)
    subcategory2 = serializers.CharField(source="subcategory2.name", read_only=True)

    class Meta:
        model = Product
        fields = ['id','name','brand','category','subcategory1','subcategory2']


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ['name']


class ProductDetailsSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    size = SizeSerializer(read_only=True, many=True)
    color = serializers.CharField(source="color.code", read_only=True)

    class Meta:
        model = ProductDetail
        fields = [
            'id',
            'product',
            'size',
            'color',
            'description',
            'mrp',
            'discount',
            'stocks',
            'image1',
            'image2',
            'image3'
        ]


class CartSerializer(serializers.ModelSerializer):
    
    user = serializers.CharField(source="user.email", read_only=True)
    product = ProductDetailsSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','product','quantity']


class RegenerateAccessTokenSerializer(serializers.Serializer):

    grant_type = serializers.CharField(error_messages={'required':'grant type may not be blank'})
    refresh_token = serializers.CharField(error_messages={'required':'refresh token may not be blank'})
