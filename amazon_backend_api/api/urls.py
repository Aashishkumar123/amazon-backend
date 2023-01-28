from django.urls import path
from amazon_backend_api.api import views


urlpatterns = [
    path('user/register/',views.RegisterAPIView.as_view(), name="amz-user-register"),
    path('user/sign-in/',views.SigninAPIView.as_view(), name="amz-user-sign-in"),
]
