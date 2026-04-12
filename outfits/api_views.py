from rest_framework.generics import ListAPIView

from outfits.models import Outfit
from outfits.serializers import OutfitSerializer


class OutfitListAPIView(ListAPIView):
    serializer_class = OutfitSerializer
    queryset = Outfit.objects.all()
