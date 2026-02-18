"""
Custom validators for the wardrobe application.

This module contains reusable validators for form and model field validation.
"""

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:
    """
    Validator to ensure uploaded images don't exceed a maximum file size.

    The maximum size is set to 5MB by default.

    Attributes:
        message (str): Error message to display when validation fails.

    Example:
        image = models.ImageField(
            validators=[ImageSizeValidator("Image size should not exceed 5MB")]
        )
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the validator with a custom error message.

        Args:
            message: The error message to display when validation fails.
        """
        self.message = message

    def __call__(self, image) -> None:
        """
        Validate the image file size.

        Args:
            image: The uploaded image file to validate.

        Raises:
            ValidationError: If the image exceeds 5MB.
        """
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(self.message)
