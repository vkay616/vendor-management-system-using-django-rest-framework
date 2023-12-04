from django.urls import path, include
from . import views


urlpatterns = [
    path("vendors/", views.VendorView.as_view(), name="vendor-list"),
    path("vendors/<int:pk>/", views.VendorView.as_view(), name="vendor-by-id"),
    path("purchase_orders/", views.PurchaseOrderView.as_view(), name="order-list"),
    path("purchase_orders/<int:pk>/", views.PurchaseOrderView.as_view(), name="order-by-id"),
    path("vendors/<int:pk>/performance/", views.HistoricalPerformanceView.as_view(), name="historical-performance"),
    path("purchase_orders/<int:pk>/acknowledge/", views.AcknowledgmentView.as_view(), name="acknowledge"),
]