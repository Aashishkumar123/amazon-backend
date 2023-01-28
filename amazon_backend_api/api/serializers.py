from rest_framework import serializers
from amazon_backend_api.models import Amazonuser


class AmazonuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amazonuser
        fields = ['email','full_name','password']
