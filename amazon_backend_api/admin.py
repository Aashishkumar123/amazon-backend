from django.contrib import admin
from amazon_backend_api.models import (
    Amazonuser,
    UserAddress
)

admin.site.register(Amazonuser)
admin.site.register(UserAddress)
