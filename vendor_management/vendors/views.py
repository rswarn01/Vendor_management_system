from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, F
from .models import Vendor, PurchaseOrder
from .serializers import (
    VendorSerializer,
    VendorUpdateSerializer,
    PurchaseOrderSerializer,
    PurchaseOrderUpdateSerializer,
    HistoricalPerformanceSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.timezone import now
from .utils import update_vendor_metrics
from rest_framework.response import Response
from datetime import timedelta


class VendorViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer},
    )
    def create(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all vendors",
        responses={200: VendorSerializer(many=True)},
    )
    def list(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Retrieve a specific vendor's details",
        responses={200: VendorSerializer},
    )
    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response("Vendor doesn't exist", status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a vendor's details",
        request_body=VendorUpdateSerializer,
        responses={200: VendorUpdateSerializer},
    )
    def update(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(
                "something went wrong, couldn't update vendor details",
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = VendorUpdateSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a vendor", responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response("Failed to delete vendor", status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(
            "Vendor Deleted Successfully", status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        operation_description="Retrieve a vendor's performance metrics",
        responses={
            200: openapi.Response(
                description="Vendor performance metrics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "on_time_delivery_rate": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="float"
                        ),
                        "quality_rating_avg": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="float"
                        ),
                        "average_response_time": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="float"
                        ),
                        "fulfillment_rate": openapi.Schema(
                            type=openapi.TYPE_NUMBER, format="float"
                        ),
                    },
                ),
            )
        },
    )
    def performance_metrics(self, vendor):
        # On-Time Delivery Rate
        completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status="completed"
        )
        on_time_deliveries = completed_orders.filter(
            delivery_date__lte=F("delivery_date")
        ).count()
        total_completed_orders = completed_orders.count()
        on_time_delivery_rate = (
            (on_time_deliveries / total_completed_orders) * 100
            if total_completed_orders != 0
            else 0
        )

        # Quality Rating Average
        quality_rating_avg = (
            completed_orders.aggregate(avg_quality_rating=Avg("quality_rating"))[
                "avg_quality_rating"
            ]
            or 0.0
        )

        # Average Response Time
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        )
        response_times = acknowledged_orders.annotate(
            response_time=F("acknowledgment_date") - F("issue_date")
        ).values_list("response_time", flat=True)
        average_response_time = (
            sum(response_times, timedelta()) / len(response_times)
            if len(response_times) != 0
            else timedelta()
        )

        # Fulfilment Rate
        fulfilled_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status="completed"
        ).count()
        total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfillment_rate = (
            (fulfilled_orders / total_orders) * 100 if total_orders != 0 else 0
        )

        return {
            "on_time_delivery_rate": round(on_time_delivery_rate, 2),
            "quality_rating_avg": round(quality_rating_avg, 2),
            "average_response_time": str(average_response_time),
            "fulfillment_rate": round(fulfillment_rate, 2),
        }

    def get_performance(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        performance_metrics = self.performance_metrics(vendor)
        return Response(performance_metrics)


class PurchaseOrderViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Create a new purchase order",
        request_body=PurchaseOrderSerializer,
        responses={201: PurchaseOrderSerializer},
    )
    def create(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all purchase orders with an option to filter by vendor",
        manual_parameters=[
            openapi.Parameter(
                "vendor",
                openapi.IN_QUERY,
                description="Vendor ID to filter by",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: PurchaseOrderSerializer(many=True)},
    )
    def list(self, request):
        vendor_id = request.query_params.get("vendor", None)
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific purchase order",
        responses={200: PurchaseOrderSerializer},
    )
    def retrieve(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response("order doesn't exists", status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a purchase order",
        request_body=PurchaseOrderUpdateSerializer,
        responses={200: PurchaseOrderUpdateSerializer},
    )
    def update(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderUpdateSerializer(
            purchase_order, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            "Failed to update details",
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a purchase order", responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response("Vendor doesn't exist", status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Acknowledge a purchase order",
        responses={200: "Acknowledged"},
    )
    def acknowledge(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        purchase_order.acknowledgment_date = now()
        purchase_order.status = "acknowledged"
        purchase_order.save()
        # Trigger metric update for vendor
        update_vendor_metrics(purchase_order.vendor)
        return Response(status=status.HTTP_200_OK)
