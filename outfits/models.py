from django.core.validators import MinLengthValidator
from django.db import models

import wardrobe.models
from core.choices import SeasonChoices
from wardrobe.validators import ImageSizeValidator


class Outfit(models.Model):
    """
    Represents a curated combination of garments for a specific occasion.

    Attributes:
        title (str): The name of the outfit.
        occasion (str): The event or situation the outfit is designed for.
        season (str): The season the outfit is suitable for.
        notes (str): Optional additional notes about the outfit.
        image (ImageField): Optional image showcasing the outfit.
        created_at (DateTime): Timestamp of when the outfit was created.
        garments (ManyToMany): Collection of garments that make up this outfit.
    """

    title = models.CharField(
        max_length=120,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2, "Title must be at least 2 characters long!")],
    )
    occasion = models.CharField(max_length=50, blank=False, null=False)
    season = models.CharField(
        choices=SeasonChoices, default=SeasonChoices.ALL, blank=False, null=False
    )
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="outfits/",
        validators=[ImageSizeValidator("Image size should not exceed 5MB!")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    garments = models.ManyToManyField(
        "wardrobe.Garment",
        through="OutfitGarment",
        related_name="outfits",
        blank=False,
    )

    def __str__(self) -> str:
        """Return a string representation combining title, occasion, and season."""
        return self.title + " - " + self.occasion + " - " + self.season


class OutfitGarment(models.Model):
    """
    Through model representing the many-to-many relationship between Outfit and Garment.

    Ensures each garment can only be added once per outfit through a unique constraint.

    Attributes:
        outfit (Outfit): Foreign key reference to the outfit.
        garment (Garment): Foreign key reference to the garment.
    """

    outfit = models.ForeignKey(
        to=Outfit, blank=False, null=False, on_delete=models.CASCADE
    )
    garment = models.ForeignKey(
        to=wardrobe.models.Garment, blank=False, null=False, on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=["outfit", "garment"], name="uniq_outfit_garment"
            )
        ]

    def __str__(self) -> str:
        """Return a string representation combining outfit and garment titles."""
        return self.outfit.title + " - " + self.garment.title
