from django.core.validators import MinLengthValidator
from django.db import models

import wardrobe.models
from wardrobe.validators import ImageSizeValidator
from outfits.choices import SeasonChoices, RoleChoices

# Create your models here.

class Outfit(models.Model):

    title = models.CharField(
        max_length=120,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2, "Title must be at least 2 characters long!")
        ]
    )
    occasion = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    season = models.CharField(
        choices=SeasonChoices,
        default=SeasonChoices.ALL,
        blank=False,
        null=False
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='outfits/',
        validators=[ImageSizeValidator("Image size should not exceed 5MB!")]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    garments = models.ManyToManyField(
        'wardrobe.Garment',
        through='OutfitGarment',
        related_name='outfits',
        blank=False,
    )

    def __str__(self):
        return self.title + ' - ' + self.occasion + ' - ' +  self.season

class OutfitGarment(models.Model):

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
        return self.outfit.title + ' - ' + self.garment.title + ' - ' + self.role