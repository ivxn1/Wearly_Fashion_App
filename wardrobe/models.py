from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from core.choices import SeasonChoices
from wardrobe.choices import GARMENT_CATEGORY_CHOICES
from wardrobe.validators import ImageSizeValidator


class Brand(models.Model):
    """
    Represents a fashion brand in the wardrobe system.

    Attributes:
        name (str): The unique name of the brand.
        website (str): Optional URL to the brand's official website.
        country (str): Optional country of origin for the brand.
    """

    name = models.CharField(max_length=80, unique=True, blank=False, null=False)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        """Return the brand name as string representation."""
        return self.name


class Garment(models.Model):
    """
    Represents a clothing item or accessory in the user's wardrobe.

    Attributes:
        category (str): The type of garment (e.g., 'tshirt', 'jeans').
        title (str): The name/title of the garment.
        brand (Brand): Foreign key reference to the associated brand.
        slug (str): URL-friendly identifier, auto-generated from title and brand.
        color (str): The primary color of the garment.
        size (str): Optional size indicator.
        material (str): Optional material composition.
        season (str): The season the garment is suitable for.
        price (Decimal): Optional purchase price.
        image (ImageField): Optional image of the garment.
        created_at (DateTime): Timestamp of when the garment was added.
    """

    category = models.CharField(
        max_length=30,
        choices=GARMENT_CATEGORY_CHOICES,
    )

    title = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2, "Title must be at least 2 characters long!")],
        blank=False,
        null=False,
    )
    brand = models.ForeignKey(
        to=Brand,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="wardrobe",
    )

    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    color = models.CharField(max_length=30, blank=False, null=False)
    size = models.CharField(max_length=10, blank=True, null=True)
    material = models.CharField(max_length=40, blank=True, null=True)
    season = models.CharField(choices=SeasonChoices, default=SeasonChoices.ALL)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0, "Price must be at least 0")],
    )
    image = models.ImageField(
        upload_to="wardrobe/",
        blank=True,
        null=True,
        validators=[
            ImageSizeValidator("Image size should not exceed 5MB"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("category", "brand")),
            models.Index(fields=("season",)),
        ]

    def save(self, *args, **kwargs) -> None:
        """
        Save the garment instance, auto-generating slug if not provided.

        The slug is created from the title and brand name using Django's slugify.
        """
        if not self.slug:
            slug = slugify(self.title + "-" + self.brand.name)
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return a string representation combining title, brand, and category."""
        return self.title + " - " + self.brand.name + " - " + self.category
