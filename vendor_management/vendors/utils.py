from datetime import timedelta
from django.db.models import F, Avg
from .models import Vendor, PurchaseOrder


def update_vendor_metrics(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor).exclude(
        acknowledgment_date__isnull=True
    )
    all_orders = PurchaseOrder.objects.filter(vendor=vendor)

    if completed_orders.exists():
        on_time_deliveries = completed_orders.filter(
            delivery_date__lte=F("delivery_date")
        ).count()
        vendor.on_time_delivery_rate = (
            on_time_deliveries / completed_orders.count() * 100
        )

        vendor.quality_rating_avg = (
            completed_orders.aggregate(Avg("quality_rating"))["quality_rating__avg"]
            or 0.0
        )

    if acknowledged_orders.exists():
        response_times = acknowledged_orders.annotate(
            response_time=F("acknowledgment_date") - F("issue_date")
        ).values_list("response_time", flat=True)
        response_times_seconds = [
            response.total_seconds() for response in response_times
        ]
        vendor.average_response_time = sum(response_times_seconds) / len(
            response_times_seconds
        )

    if all_orders.exists():
        fulfilled_orders = all_orders.filter(status="completed").count()
        vendor.fulfillment_rate = fulfilled_orders / all_orders.count() * 100

    vendor.save()
