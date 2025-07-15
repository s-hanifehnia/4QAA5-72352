from django.urls import reverse
from django.test import override_settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Table, Reservation

User = get_user_model()


@override_settings(SEAT_PRICE=1000)
class CancelingTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.login(username="test", password="test")
        self.table = Table.objects.create(name="#01", seats=4)
        self.book_url = reverse("booking:book")
        self.client.post(self.book_url, {"requested_seats": 4})
        self.reservation = Reservation.objects.get(user=self.user)
        self.cancel_url = reverse("booking:cancel", args=[self.reservation.pk])

    def test_cancel_reservation_success(self):
        response = self.client.delete(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, Reservation.Status.CANCELLED)

    def test_cancel_reservation_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_non_active_reservation(self):
        self.reservation.status = Reservation.Status.CANCELLED
        self.reservation.save()
        response = self.client.delete(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_other_user_reservation(self):
        User.objects.create_user(username="other", password="other")
        self.client.login(username="other", password="other")
        response = self.client.delete(self.cancel_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
