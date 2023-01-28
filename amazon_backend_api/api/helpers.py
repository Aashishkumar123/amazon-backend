from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


JWT_authenticator = JWTAuthentication()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'email' : user.email,
        'full name' : user.full_name,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_token(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        user , token = response
        return user
