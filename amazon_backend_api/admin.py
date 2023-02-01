from django.contrib import admin
from amazon_backend_api.models import (
    Amazonuser,
    UserAddress,
    Brand,
    Category,
    Subcategory,
    Size
)

admin.site.register(Amazonuser)
admin.site.register(UserAddress)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Size)
