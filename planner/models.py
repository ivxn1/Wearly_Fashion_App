from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

import outfits.models

UserModel = get_user_model()

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

    date = models.DateField(blank=False, null=False)
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
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="plans"
    )

    class Meta:
        ordering = ("date",)
        constraints = [
            models.UniqueConstraint(
                fields=["date", "user"], name="uniq_plan_user_date_constraint"
            )
        ]
        indexes = [models.Index(fields=("date",))]
        verbose_name_plural = "Plan Entries"
        verbose_name = "Plan Entry"

    def __str__(self) -> str:
        """Return a string representation combining date, outfit title, and creation time."""
        return str(self.date) + " - " + self.outfit.title + " - " + str(self.created_at)
