from django.urls import path
from .views import VendorViewSet, PurchaseOrderViewSet

vendor_list = VendorViewSet.as_view({"get": "list", "post": "create"})

vendor_detail = VendorViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

vendor_performance = VendorViewSet.as_view({"get": "get_performance"})

purchase_order_list = PurchaseOrderViewSet.as_view({"get": "list", "post": "create"})

purchase_order_detail = PurchaseOrderViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)

purchase_order_acknowledge = PurchaseOrderViewSet.as_view({"post": "acknowledge"})

urlpatterns = [
    path("vendors/", vendor_list, name="vendor-list"),
    path("vendors/<int:pk>/", vendor_detail, name="vendor-detail"),
    path(
        "vendors/<int:pk>/performance/", vendor_performance, name="vendor-performance"
    ),
    path("purchase_orders/", purchase_order_list, name="purchase-order-list"),
    path(
        "purchase_orders/<int:pk>/", purchase_order_detail, name="purchase-order-detail"
    ),
    path(
        "purchase_orders/<int:pk>/acknowledge/",
        purchase_order_acknowledge,
        name="purchase-order-acknowledge",
    ),
]
