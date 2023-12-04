from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vendor

        fields = "__all__"

        read_only_fields = [
            "id",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate"
        ]



class POSerializer(serializers.ModelSerializer):

    class Meta:

        model = PurchaseOrder

        fields = "__all__"

        read_only_fields = [
            "order_date"
        ]


class HPSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = HistoricalPerformance

        fields = "__all__"