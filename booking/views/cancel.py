from rest_framework.generics import DestroyAPIView

from booking.models import Reservation


class CancelDestroyView(DestroyAPIView):

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user, status=Reservation.Status.ACTIVE
        )

    def perform_destroy(self, instance):
        instance.status = Reservation.Status.CANCELLED
        instance.save()
