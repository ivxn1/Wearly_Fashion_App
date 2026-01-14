from django.core.validators import MinLengthValidator
from django.db import models

import wardrobe.models


# Create your models here.

class Occasion(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name

class Outfit(models.Model):

    class SeasonChoices(models.TextChoices):
        ALL = 'all', 'All-Season'
        SPRING = 'spring', 'Spring'
        SUMMER = 'summer', 'Summer'
        AUTUMN = 'autumn', 'Autumn'
        WINTER = 'winter', 'Winter'

    title = models.CharField(
        max_length=120,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2, "Title must be at least 2 characters long!")
        ]
    )
    occasion = models.ForeignKey(
        to=Occasion,
        blank=False,
        null=False,
        on_delete=models.PROTECT
    )
    season = models.CharField(
        choices=SeasonChoices,
        default=SeasonChoices.ALL
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='outfits/'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title + self.occasion.name + self.season

class OutfitGarment(models.Model):

    class RoleChoices(models.TextChoices):
        TOP = 'top', 'Top'
        BOTTOM = 'bottom', 'Bottom'
        SHOES = 'shoes', 'Shoes'
        OUTERWEAR = 'outerwear', 'Outerwear'
        ACCESSORY = 'accessory', 'Accessory'

    outfit = models.ForeignKey(
        to=Outfit,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    garment = models.ForeignKey(
        to=wardrobe.models.Garment,
        blank=False,
        null=False,
        on_delete=models.PROTECT
    )
    role = models.CharField(
        choices=RoleChoices,
        blank=False,
        null=False
    )
    order = models.IntegerField(
        default=1
    )
    is_key_piece = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ('order', 'id')
        constraints = [
            models.UniqueConstraint(
                fields=['outfit', 'garment'],
                name='uniq_outfit_garment'
            )
        ]

    def __str__(self):
        return self.outfit.title + self.garment.title + self.role