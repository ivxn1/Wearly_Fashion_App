from django.core.validators import MinLengthValidator
from django.db import models

import outfits.models


class PlanEntry(models.Model):
    """
    Represents a scheduled outfit plan for a specific date.

    Each date can only have one plan entry (enforced by unique constraint).

    Attributes:
        date (Date): The date for this planned outfit (unique).
        outfit (Outfit): Foreign key reference to the planned outfit.
        note (str): Optional note about the plan (5-200 characters).
        created_at (DateTime): Timestamp of when the plan was created.
    """

    date = models.DateField(unique=True, blank=False, null=False)
    outfit = models.ForeignKey(
        to=outfits.models.Outfit,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="planentry",
    )
    note = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        validators=[MinLengthValidator(5, "Note must be at least 5 characters long!")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date",)
        indexes = [models.Index(fields=("date",))]
        verbose_name_plural = "Plan Entries"
        verbose_name = "Plan Entry"

    def __str__(self) -> str:
        """Return a string representation combining date, outfit title, and creation time."""
        return str(self.date) + " - " + self.outfit.title + " - " + str(self.created_at)
