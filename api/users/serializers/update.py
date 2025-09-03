from .base import BaseUserSerializer


class UpdateUserSerializer(BaseUserSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def validate(self, attrs):
        user = self.context['user']

        if attrs.get('username') == user.username:
            attrs.pop('username')

        return attrs