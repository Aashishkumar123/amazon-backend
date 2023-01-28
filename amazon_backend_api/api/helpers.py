from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'email' : user.email,
        'full name' : user.full_name,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
