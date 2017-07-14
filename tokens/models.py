from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Token(models.Model):
    public_name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=4)
    decimals = models.IntergerField(
        default=18,
        validators=[MaxValueValidator(20), MinValueValidator(0)]
    )
