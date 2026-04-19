from django.urls.conf import path

from outfits.api_views import OutfitListAPIView

urlpatterns = [
    path("", OutfitListAPIView.as_view(), name="outfit-api-list"),
]
