from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from wardrobe.models import Garment, Brand


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'website', 'country']

class GarmentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    brand = BrandSerializer()

    class Meta:
        model = Garment
        fields = ['title', 'category', 'brand', 'price', 'slug', 'color', 'size', 'season', 'material', 'created_at', 'user']

