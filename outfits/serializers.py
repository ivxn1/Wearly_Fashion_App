from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from outfits.models import Outfit
from wardrobe.serializers import GarmentSerializer


class OutfitSerializer(ModelSerializer):
    garments = GarmentSerializer(many=True)
    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["garments_count"] = instance.garments.count()
        return representation

    class Meta:
        model = Outfit
        fields = [
            "title",
            "occasion",
            "season",
            "notes",
            "created_at",
            "user",
            "garments",
        ]
