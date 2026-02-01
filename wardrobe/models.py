from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from wardrobe.choices import SeasonChoices, GARMENT_CATEGORY_CHOICES


# Create your models here.

class Brand(models.Model):

    name = models.CharField(
        max_length=80,
        unique=True,
        blank=False,
        null=False
    )
    website = models.URLField(
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Garment(models.Model):

    category = models.CharField(
        max_length=30,
        choices=GARMENT_CATEGORY_CHOICES,
    )

    title = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(
                2,
                'Title must be at least 2 characters long!'
            )
        ],
        blank=False,
        null=False
    )
    brand = models.ForeignKey(
        to=Brand,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name='wardrobe'
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )
    size = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    material = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    season = models.CharField(
        choices=SeasonChoices,
        default=SeasonChoices.ALL
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators = [
            MinValueValidator(0, 'Price must be at least 0')
        ]
    )
    image = models.ImageField(
        upload_to='wardrobe/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=('category', 'brand')),
            models.Index(fields=('season',))
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title + '-' + self.brand.name)
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title + ' - ' + self.brand.name + ' - ' + self.category