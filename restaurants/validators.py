from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            '%(value)s is not an even number',
            params={'value': value},
        )


CATEGORIES = ['Mexican', 'Asian', 'American', 'Whatever']


def validate_category(value):
    if not value.capitalize() in CATEGORIES:
        raise ValidationError(f"{value} not a valid category")
