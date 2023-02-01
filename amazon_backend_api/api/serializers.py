from rest_framework import serializers
from amazon_backend_api.models import Amazonuser, UserAddress, Brand
from rest_framework.serializers import ALL_FIELDS


class AmazonuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amazonuser
        fields = ['email','full_name','password']


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
