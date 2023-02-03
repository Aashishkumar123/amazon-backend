from django.urls import path,re_path
from amazon_backend_api.api import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('user/register/',views.RegisterAPIView.as_view(), name="amz-user-register"),
    path('user/sign-in/',views.SigninAPIView.as_view(), name="amz-user-sign-in"),
    path('user/address/',views.UserAddressAPIView.as_view(),name='amz-user-address'),
    path('user/address/set/default/<int:id>/',views.SetdefaultAddressAPIView.as_view(),name='amz-user-address-set-default'),
    path('brands/',views.BrandAPIView.as_view(),name="amz-brands"),
    path('products/fashion/<str:subcategory1>/',views.ProductsAPIView.as_view(),name="amz-products-subcategory1"),
    path('products/fashion/<str:subcategory1>/<str:subcategory2>/',views.ProductsAPIView.as_view(),name="amz-products-subcategory2"),
    path('product/product-id/<int:product_id>/product-detail/<int:product_detail_id>/',views.ProductDetailsAPIView.as_view(),name="amz-product-details"),
    path('cart/',views.CartAPIView.as_view(),name="amz-cart"),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
