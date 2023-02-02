from django.urls import path
from amazon_backend_api.api import views


urlpatterns = [
    path('user/register/',views.RegisterAPIView.as_view(), name="amz-user-register"),
    path('user/sign-in/',views.SigninAPIView.as_view(), name="amz-user-sign-in"),
    path('user/address/',views.UserAddressAPIView.as_view(),name='amz-user-address'),
    path('user/address/set/default/<int:id>/',views.SetdefaultAddressAPIView.as_view(),name='amz-user-address-set-default'),
    path('brands/',views.BrandAPIView.as_view(),name="amz-brands"),
    path('products/fashion/<str:subcategory1>/',views.ProductsAPIView.as_view(),name="amz-products-subcategory1"),
    path('products/fashion/<str:subcategory1>/<str:subcategory2>/',views.ProductsAPIView.as_view(),name="amz-products-subcategory2"),
    path('product/product-id/<int:product_id>/product-detail/<int:product_detail_id>/',views.ProductDetailsAPIView.as_view(),name="amz-product-details"),
]
