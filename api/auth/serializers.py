from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if hasattr(self.user, 'is_verified') and not self.user.is_verified:
            raise AuthenticationFailed("User is not verified.")

        return data
