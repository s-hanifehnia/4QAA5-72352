from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

UserModel = get_user_model()


class Reservation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="reservations"
    )
    table = models.ForeignKey(
        "Table", on_delete=models.PROTECT, related_name="reservations"
    )
    requested_seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    reserved_seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)]
    )
    cost = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Table {self.table}"
