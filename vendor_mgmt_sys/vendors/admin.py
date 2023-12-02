from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_details",
        "vendor_code",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate"
    )


admin.site.register(Vendor, VendorAdmin)


class POAdmin(admin.ModelAdmin):
    list_display = (
        "po_number",
        "vendor",
        "order_date",
        "status",
        "quantity"
    )


admin.site.register(PurchaseOrder, POAdmin)


class HPAdmin(admin.ModelAdmin):
    list_display = (
        "vendor",
        "date",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate"
    )


admin.site.register(HistoricalPerformance, HPAdmin)