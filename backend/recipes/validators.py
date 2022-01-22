from django.core.exceptions import ValidationError


def number_validator(value):
    if value < 1:
        raise ValidationError(
            ('%s is not a correct number!' % value))
