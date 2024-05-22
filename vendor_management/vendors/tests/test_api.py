from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Vendor, PurchaseOrder


class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="1234",
        )

    def test_create_vendor(self):
        url = reverse("vendor-list")
        data = {
            "name": "New Vendor",
            "contact_details": "New Contact",
            "address": "New Address",
            "vendor_code": "5678",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_list_vendors(self):
        url = reverse("vendor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        url = reverse("vendor-detail", args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse("vendor-detail", args=[self.vendor.pk])
        data = {"name": "Updated Vendor"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, "Updated Vendor")


class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact",
            address="Address",
            vendor_code="1234",
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=self.vendor,
            order_date="2024-05-22T12:00:00Z",
            delivery_date="2024-05-30T12:00:00Z",
            items={},
            quantity=10,
            status="pending",
            issue_date="2024-05-22T12:00:00Z",
        )

    def test_create_purchase_order(self):
        url = reverse("purchase-order-list")
        data = {
            "po_number": "PO456",
            "vendor": self.vendor.pk,
            "order_date": "2024-06-01T12:00:00Z",
            "delivery_date": "2024-06-10T12:00:00Z",
            "items": {},
            "quantity": 5,
            "status": "pending",
            "issue_date": "2024-06-01T12:00:00Z",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_list_purchase_orders(self):
        url = reverse("purchase-order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        url = reverse("purchase-order-detail", args=[self.purchase_order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse("purchase-order-detail", args=[self.purchase_order.pk])
        data = {"quantity": 15}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.quantity, 15)

    def test_delete_purchase_order(self):
        url = reverse("purchase-order-detail", args=[self.purchase_order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        url = reverse("purchase-order-acknowledge", args=[self.purchase_order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)
