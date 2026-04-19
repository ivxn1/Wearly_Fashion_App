from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from accounts.models import CustomerProfileModel, FavouriteOutfits, Wishlist

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfileModel.objects.create(user=instance)
        Wishlist.objects.create(user=instance)
        FavouriteOutfits.objects.create(user=instance)
