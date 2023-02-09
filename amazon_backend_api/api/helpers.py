from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from amazon_backend_api.models import Amazonuser


JWT_authenticator = JWTAuthentication()


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        "email": user.email,
        "full name": user.full_name,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_from_token(request):

    response = JWT_authenticator.authenticate(request)

    if response is not None:
        user, token = response
        return user


def get_access_token_from_refresh_token(request):

    if request.data["grant_type"] == "refresh_token":
        access_token = RefreshToken(request.data["refresh_token"]).access_token
        request.META["HTTP_AUTHORIZATION"] = "Bearer " + str(access_token)
        user = get_user_from_token(request)
        data = get_tokens_for_user(Amazonuser.objects.get(email=user))
        return data
    return None
