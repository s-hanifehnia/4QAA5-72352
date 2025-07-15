from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Table(models.Model):
    name = models.CharField(max_length=20, unique=True)
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(10)]
    )

    def __str__(self) -> str:
        return f"{self.name}"
