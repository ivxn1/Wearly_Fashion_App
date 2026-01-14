from django.core.validators import MinLengthValidator
from django.db import models

import outfits.models


# Create your models here.

class PlanEntry(models.Model):
    date = models.DateField(
        unique=True,
        blank=False,
        null=False
    )
    outfit = models.ForeignKey(
        to=outfits.models.Outfit,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name = 'planentry'
    )
    note = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(5, "Note must be at least 5 characters long!")
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('-date',)
        indexes = [
            models.Index(fields=('date',))
        ]
        verbose_name_plural = 'Plan Entries'
        verbose_name = 'Plan Entry'

    def __str__(self):
        return str(self.date) + ' - '+  self.outfit.title + ' - '+ str(self.created_at)