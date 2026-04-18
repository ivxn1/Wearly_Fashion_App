from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["first_name"] = instance.profile.first_name
        representation["last_name"] = instance.profile.last_name
        return representation
