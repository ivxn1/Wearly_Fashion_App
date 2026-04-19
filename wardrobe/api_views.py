from rest_framework.generics import ListAPIView

from wardrobe.models import Garment
from wardrobe.serializers import GarmentSerializer


class GarmentListAPIView(ListAPIView):
    queryset = Garment.objects.all()
    serializer_class = GarmentSerializer
