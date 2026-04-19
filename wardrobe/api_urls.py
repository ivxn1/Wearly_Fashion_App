from django.urls.conf import path

from wardrobe.api_views import GarmentListAPIView

urlpatterns = [
    path("", GarmentListAPIView.as_view(), name="garment-api-list"),
]
