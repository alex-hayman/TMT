from datetime import datetime, timedelta
from django.test import TestCase
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class InventoryTestCase(TestCase):
    def setUp(self):
        self.language = InventoryLanguage.objects.create(name="English")
        self.inv_type = InventoryType.objects.create(name="Movie")
        self.inventory = Inventory.objects.create(
            name="Test Movie",
            language=self.language,
            type=self.inv_type,
            metadata={"year": 2024}
        )

    def test_get_created_after(self):
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        # Should find the item (created after yesterday)
        results = Inventory.get_created_after(yesterday)
        self.assertEqual(results.count(), 1)

        # Should not find the item (created before tomorrow)
        results = Inventory.get_created_after(tomorrow)
        self.assertEqual(results.count(), 0)
