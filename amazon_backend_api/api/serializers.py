from rest_framework import serializers
from amazon_backend_api.models import Amazonuser, UserAddress


class AmazonuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amazonuser
        fields = ['email','full_name','password']


class AmazonuserAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = UserAddress
        fields = [
            'user',
            'country',
            'full_name',
            'mobile_number',
            'pincode',
            'flat',
            'street',
            'landmark',
            'town',
            'state',
            'default',
            'address_type',   
        ]
