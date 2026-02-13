from datetime import date, timedelta
from rest_framework.test import APITestCase
from rest_framework import status

from interview.order.models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class OrdersByDateRangeViewTestCase(APITestCase):
    def setUp(self):
        self.language = InventoryLanguage.objects.create(name="English")
        self.inv_type = InventoryType.objects.create(name="Movie")
        self.inventory = Inventory.objects.create(
            name="Test Movie",
            language=self.language,
            type=self.inv_type,
            metadata={"year": 2024}
        )
        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2024, 1, 15),
            embargo_date=date(2024, 2, 15)
        )
        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2024, 3, 1),
            embargo_date=date(2024, 4, 1)
        )
        self.order3 = Order.objects.create(
            inventory=self.inventory,
            start_date=date(2024, 6, 1),
            embargo_date=date(2024, 12, 31)
        )

    def test_orders_by_date_range_success(self):
        response = self.client.get(
            "/orders/by-date-range/",
            {"start_date": "2024-01-01", "embargo_date": "2024-05-01"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_orders_by_date_range_no_results(self):
        response = self.client.get(
            "/orders/by-date-range/",
            {"start_date": "2025-01-01", "embargo_date": "2025-12-31"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_orders_by_date_range_missing_start_date(self):
        response = self.client.get(
            "/orders/by-date-range/",
            {"embargo_date": "2024-12-31"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_orders_by_date_range_missing_embargo_date(self):
        response = self.client.get(
            "/orders/by-date-range/",
            {"start_date": "2024-01-01"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_orders_by_date_range_missing_both_params(self):
        response = self.client.get("/orders/by-date-range/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
