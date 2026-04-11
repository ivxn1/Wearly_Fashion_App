"""
Shared choice definitions for the Wearly application.

This module contains TextChoices enums that are used across
multiple apps in the project.
"""

from django.db import models


class SeasonChoices(models.TextChoices):
    """
    Enumeration of season options for garments and outfits.

    Includes an 'All Seasons' option for items suitable year-round.
    """

    ALL = "", "All Seasons"
    SPRING = "spring", "Spring"
    SUMMER = "summer", "Summer"
    AUTUMN = "autumn", "Autumn"
    WINTER = "winter", "Winter"

class StylePreferencesChoices(models.TextChoices):
    CASUAL = "casual", "Casual"
    FORMAL = "formal", "Formal"
    STREETWEAR = "streetwear", "Streetwear"
    MINIMALIST = "minimalist", "Minimalist"
    ECLECTIC = "eclectic", "Eclectic"