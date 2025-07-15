from django.urls import reverse
from django.conf import settings
from django.test import override_settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Table

User = get_user_model()


@override_settings(SEAT_PRICE=1000)
class BookingTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.login(username="test", password="test")
        self.book_url = reverse("booking:book")
        Table.objects.create(name="#01", seats=4)
        Table.objects.create(name="#02", seats=5)
        Table.objects.create(name="#03", seats=6)

    def test_successful_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("reservation_id", response.data)

    def test_low_cost_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 2)
        self.assertEqual(response.data["table"], "#01")

    def test_second_low_cost_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 2)
        self.assertEqual(response.data["table"], "#01")
        response = self.client.post(self.book_url, {"requested_seats": 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 2)
        self.assertEqual(response.data["table"], "#02")

    def test_odd_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 2)
        self.assertEqual(response.data["table"], "#01")

    def test_full_table_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 3)
        self.assertEqual(response.data["table"], "#01")

    def test_full_table_odd_booking(self):
        response = self.client.post(self.book_url, {"requested_seats": 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 3)
        self.assertEqual(response.data["table"], "#01")
        response = self.client.post(self.book_url, {"requested_seats": 5})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["cost"], settings.SEAT_PRICE * 4)
        self.assertEqual(response.data["table"], "#02")

    def test_booking_no_table_available(self):
        for _ in range(3):
            self.client.post(self.book_url, {"requested_seats": 4})
        response = self.client.post(self.book_url, {"requested_seats": 4})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No table found.", str(response.data))

    def test_booking_no_seat_available(self):
        response = self.client.post(self.book_url, {"requested_seats": 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No table found.", str(response.data))

    def test_booking_with_bad_requested_seats(self):
        response = self.client.post(self.book_url, {"requested_seats": 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.book_url, {"requested_seats": 11})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(self.book_url, {"requested_seats": 4})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
