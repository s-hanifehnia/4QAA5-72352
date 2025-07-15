from django.db import models, transaction
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Table(models.Model):
    name = models.CharField(max_length=20, unique=True)
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(10)]
    )

    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def find_available_table_for_requested_seats(cls, requested_seats: int):
        with transaction.atomic():
            return (
                cls.objects.select_for_update(skip_locked=True)
                .filter(seats__gte=requested_seats)
                .exclude(reservations__status="active")
                .order_by("seats")
                .first()
            )

    def calculate_reserved_seats(self, requested_seats: int):
        reserved_seats = requested_seats
        if requested_seats % 2 != 0 and requested_seats != self.seats:
            reserved_seats = requested_seats + 1
        return reserved_seats

    def calculate_cost(self, reserved_seats: int):
        seat_price = self.get_seat_price()
        cost = reserved_seats * seat_price
        if reserved_seats == self.seats:
            cost = (self.seats - 1) * seat_price
        return cost

    @staticmethod
    def get_seat_price():
        return settings.SEAT_PRICE
