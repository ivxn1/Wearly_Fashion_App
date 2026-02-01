from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, image):
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(self.message)
