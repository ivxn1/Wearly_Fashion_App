from django.db import models


class SeasonChoices(models.TextChoices):
    ALL = 'all', 'All-Season'
    SPRING = 'spring', 'Spring'
    SUMMER = 'summer', 'Summer'
    AUTUMN = 'autumn', 'Autumn'
    WINTER = 'winter', 'Winter'

class RoleChoices(models.TextChoices):
    TOP = 'top', 'Top'
    BOTTOM = 'bottom', 'Bottom'
    SHOES = 'shoes', 'Shoes'
    OUTERWEAR = 'outerwear', 'Outerwear'
    ACCESSORY = 'accessory', 'Accessory'
