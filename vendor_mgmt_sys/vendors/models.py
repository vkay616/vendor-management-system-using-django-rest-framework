from collections.abc import Iterable
from django.db import models
import uuid
from datetime import timedelta, datetime

# model for Vendors
class Vendor(models.Model):

    # name of the vendor
    name = models.CharField(
        max_length=100,
        blank=False,
        help_text="name of the vendor"
    )

    # contact details of the vendor
    contact_details = models.TextField(
        blank=False,
        help_text="contact details of the vendor"
    )

    # physical address of the vendor
    address = models.TextField(
        blank=False,
        help_text="address of the vendor"
    )

    # unique identifier code for the vendor
    vendor_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="unique identifier for the vendor"
    )

    # on time delivery rate of the vendor
    on_time_delivery_rate = models.FloatField(
        blank=True,
        null=True,
        help_text="percentage of on time deliveries by the vendor"
    )

    # average quality rating of the vendor
    quality_rating_avg = models.FloatField(
        blank=True,
        null=True,
        help_text="average quality rating based on purchase orders"
    )

    # average response time of the vendor
    average_response_time = models.FloatField(
        blank=True,
        null=True,
        help_text="average time taken to respond to purchase orders"
    )

    # fulfillment rate of the vendor
    fulfillment_rate = models.FloatField(
        blank=True,
        null=True,
        help_text="percentage of purchase orders fulfilled successfully"
    )


# model for Purchase Orders
class PurchaseOrder(models.Model):

    # unique identifier for order
    po_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="unique identifier for purchase order"
    )

    # vendor associated with the order
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE,
        help_text="vendor associated with the purchase order"
    )

    # date the order was placed on
    order_date = models.DateTimeField(
        auto_now_add=True,
        help_text="date and time when the order was placed"
    )

    # expected or actual date of delivery
    delivery_date = models.DateTimeField(
        default=datetime.now()+timedelta(days=3),
        help_text="expected or actual delivery date"
    )

    # items included in the order
    items = models.JSONField(
        blank=False,
        help_text="items included in the order"
    )

    # total quantity of items in the order
    quantity = models.IntegerField(
        blank=False,
        help_text="total quantity of items ordered"
    )

    # current status of the order
    status = models.CharField(
        max_length=10,
        choices=[("pending", "pending"), ("completed", "completed"), ("cancelled", "cancelled")], 
        default="pending",
        help_text="current status of the order"
    )

    # quality rating for the order
    quality_rating = models.FloatField(
        null=True,
        blank=True,
        help_text="rating for the order"
    )

    # date the order was issued to the vendor
    issue_date = models.DateTimeField(
        auto_now_add=True,
        help_text="date when the order was issued to the vendor"
    )

    # date the order was acknowledged by the vendor
    acknowledgment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="date when the order was acknowledged by the vendor"
    )


class HistoricalPerformance(models.Model):

    # the vendor whose performance is being tracked
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        help_text="the vendor whose performance is being monitored"
    )

    # the date the performance was recorded
    date = models.DateTimeField(
        auto_now_add=True,
        help_text="the date the performance was recorded"
    )

    # on time delivery rate on the recorded date
    on_time_delivery_rate = models.FloatField(
        editable=False,
        help_text="on time delivery rate on the recorded date"
    )

    # average rating of the vendor on the recorded date
    quality_rating_avg = models.FloatField(
        editable=False,
        help_text="average rating of the vendor on the recorded date"
    )

    # average response time of the vendor on the recorded date
    average_response_time = models.FloatField(
        editable=False,
        help_text="average response time of the vendor on the recorded date"
    )

    # fulfillment rate of the vendor on the recorded date
    fulfillment_rate = models.FloatField(
        editable=False,
        help_text="fulfillment rate of the vendor on the recorded date"
    )

    # automatically saves all the performance metrics at the time the performance was recorded    
    def save(self):
        self.on_time_delivery_rate = self.vendor.on_time_delivery_rate
        self.quality_rating_avg = self.vendor.quality_rating_avg
        self.average_response_time = self.vendor.average_response_time
        self.fulfillment_rate = self.vendor.fulfillment_rate
        super().save()