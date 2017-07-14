from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .conf import PHASES, TOKEN_TYPES


class Token(models.Model):
    public_name = models.CharField(max_length=200)

    symbol = models.CharField(max_length=4)

    decimals = models.IntegerField(
        default=18,
        validators=[MaxValueValidator(20), MinValueValidator(0)]
    )

    phase = models.CharField(
        max_length=8,
        choices=PHASES,
        default=PHASES[0][0],
    )

    token_type = models.CharField(
        max_length=12,
        choices=TOKEN_TYPES,
        default=TOKEN_TYPES[0][0],
    )

    @property
    def class_name(self):
        return ''.join(
            map(lambda s: s.title(), self.public_name.split())
        )