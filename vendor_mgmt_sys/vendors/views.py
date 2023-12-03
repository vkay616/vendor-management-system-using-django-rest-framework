from django.shortcuts import render
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendorSerializer
from datetime import timedelta
from rest_framework import status


def evaluate_avg_rating():
    vendors = Vendor.objects.all()
    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(vendor=vendor).filter(status="completed")
        n = len(orders)
        avg_rating = None
        if n > 1:
            s = 0
            for order in orders:
                s += order.quality_rating

            avg_rating = s / n

        elif n == 1:
            avg_rating = orders[0].quality_rating
        
        else:
            avg_rating = None
        
        vendor.quality_rating_avg = avg_rating

        vendor.save(update_fields=["quality_rating_avg"])


def evaluate_on_time_delivery_rate():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(vendor=vendor).filter(status="completed")
        n = len(orders)
        delivery_rate = None

        if n > 1:
            on_time = 0
            for order in orders:
                expected_delivery_date = order.order_date.date() + timedelta(days=3)
                if order.delivery_date.date() <= expected_delivery_date:
                    on_time += 1

            delivery_rate = (on_time / n) * 100

        elif n == 1:
            expected_delivery_date = orders[0].order_date.date() + timedelta(days=3)
            if orders[0].delivery_date.date() <= expected_delivery_date:
                delivery_rate = 100
            else:
                delivery_rate = 0
        
        else:
            delivery_rate = None

        vendor.on_time_delivery_rate = delivery_rate

        vendor.save(update_fields=["on_time_delivery_rate"])


def evaluate_response_time():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(vendor=vendor).filter(acknowledgment_date__isnull=False)
        n = len(orders)
        reponse_time = None

        if n > 1:
            t = timedelta(0)
            for order in orders:
                t += order.acknowledgment_date - order.issue_date

            response_time = t / n

        elif n == 1:
            response_time = orders[0].acknowledgment_date - orders[0].issue_date

        if response_time:
            vendor.average_response_time = (response_time.days * 24) + (response_time.seconds / 60)
        
        if n == 0:
            vendor.average_response_time = None
        

        vendor.save(update_fields=["average_response_time"])


def evaluate_fulfillment_rate():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(vendor=vendor).exclude(status="pending")
        n = len(orders)
        rate = 0

        if n > 1:
            successful_orders = orders.filter(status="completed")
            
            rate = (len(successful_orders) / n) * 100

        elif n == 1:
            if orders[0].status == "completed":
                rate = 100
            else:
                rate = 0
        
        else:
            rate = None

        vendor.fulfillment_rate = rate

        vendor.save(update_fields=["fulfillment_rate"])


def evaluate_performance():
    evaluate_avg_rating()
    evaluate_on_time_delivery_rate()
    evaluate_response_time()
    evaluate_fulfillment_rate()


class VendorView(APIView):

    def get(self, request, pk=None):
        evaluate_performance()
        if pk:
            try:
                vendor = Vendor.objects.get(id=pk)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": f"vendor with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                vendors = Vendor.objects.all()
                serializer = VendorSerializer(vendors, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk=None):
        if pk:
            try:
                vendor = Vendor.objects.get(pk=pk)
                serializer = VendorSerializer(vendor, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "there are some errors in the json body"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"vendor with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": f"enter a valid id"}, status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, pk=None):
        if pk:
            vendor = Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "enter a valid vendor id"}, status=status.HTTP_400_BAD_REQUEST)
                

    