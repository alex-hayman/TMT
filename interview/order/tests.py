from datetime import date, timedelta
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from interview.order.models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class DeactivateOrderViewTestCase(APITestCase):
    def setUp(self):
        self.language = InventoryLanguage.objects.create(name="English")
        self.inv_type = InventoryType.objects.create(name="Movie")
        self.inventory = Inventory.objects.create(
            name="Test Movie",
            language=self.language,
            type=self.inv_type,
            metadata={"year": 2024}
        )
        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date=date.today(),
            embargo_date=date.today() + timedelta(days=30),
            is_active=True
        )

    def test_deactivate_order_success(self):
        response = self.client.patch(f"/orders/{self.order.pk}/deactivate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)

    def test_deactivate_order_not_found(self):
        response = self.client.patch("/orders/99999/deactivate/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Order not found")

    def test_deactivate_already_inactive_order(self):
        self.order.is_active = False
        self.order.save()
        response = self.client.patch(f"/orders/{self.order.pk}/deactivate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
