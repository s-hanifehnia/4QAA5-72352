from django.db import transaction
from rest_framework import serializers

from booking.models import Reservation, Table


class BookSerializer(serializers.Serializer):
    requested_seats = serializers.IntegerField(min_value=1, max_value=10)

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            requested_seats = validated_data["requested_seats"]
            table = Table.find_available_table_for_requested_seats(requested_seats)
            if not table:
                raise serializers.ValidationError("No table found.")

            reserved_seats = table.calculate_reserved_seats(
                requested_seats=requested_seats
            )
            cost = table.calculate_cost(reserved_seats=reserved_seats)

            reservation = Reservation.objects.create(
                user=user,
                table=table,
                requested_seats=requested_seats,
                reserved_seats=reserved_seats,
                cost=cost,
            )
            return reservation

    def to_representation(self, instance):
        return {
            "reservation_id": instance.id,
            "table": instance.table.name,
            "requested_seats": instance.requested_seats,
            "reserved_seats": instance.reserved_seats,
            "cost": instance.cost,
            "status": instance.status,
            "created_at": instance.created_at,
        }
