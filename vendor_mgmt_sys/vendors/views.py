from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendorSerializer, POSerializer, HPSerializer
from datetime import timedelta, datetime
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# function to evaluate average quality rating
def evaluate_avg_rating():
    vendors = Vendor.objects.all()
    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(
            vendor=vendor).filter(status="completed")
        n = len(orders)
        avg_rating = None
        if n > 1:
            s = 0
            for order in orders:
                s += order.quality_rating

            avg_rating = round(s / n,2)

        elif n == 1:
            avg_rating = round(orders[0].quality_rating,2)

        else:
            avg_rating = None

        vendor.quality_rating_avg = avg_rating

        vendor.save(update_fields=["quality_rating_avg"])

# function to evaluate on time delivery rate
def evaluate_on_time_delivery_rate():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(
            vendor=vendor).filter(status="completed")
        n = len(orders)
        delivery_rate = None

        if n > 1:
            on_time = 0
            for order in orders:
                expected_delivery_date = order.order_date.date() + timedelta(days=3)
                if order.delivery_date.date() <= expected_delivery_date:
                    on_time += 1

            delivery_rate = round((on_time / n) * 100,2)

        elif n == 1:
            expected_delivery_date = orders[0].order_date.date(
            ) + timedelta(days=3)
            if orders[0].delivery_date.date() <= expected_delivery_date:
                delivery_rate = 100
            else:
                delivery_rate = 0

        else:
            delivery_rate = None

        vendor.on_time_delivery_rate = delivery_rate

        vendor.save(update_fields=["on_time_delivery_rate"])

# function to evaluate response time of the vendor
def evaluate_response_time():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(
            vendor=vendor).filter(acknowledgment_date__isnull=False)
        n = len(orders)
        reponse_time = None

        if n > 1:
            t = timedelta(0)
            for order in orders:
                t += order.acknowledgment_date - order.issue_date

            response_time = t / n

        elif n == 1:
            response_time = orders[0].acknowledgment_date - \
                orders[0].issue_date

        if response_time:
            vendor.average_response_time = round((
                response_time.days * 24) + (response_time.seconds / 60),2)

        if n == 0:
            vendor.average_response_time = None

        vendor.save(update_fields=["average_response_time"])

# function to evaluate fulfillment rate of the vendor
def evaluate_fulfillment_rate():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        orders = PurchaseOrder.objects.filter(
            vendor=vendor).exclude(status="pending")
        n = len(orders)
        rate = 0

        if n > 1:
            successful_orders = orders.filter(status="completed")

            rate = round((len(successful_orders) / n) * 100,2)

        elif n == 1:
            if orders[0].status == "completed":
                rate = 100
            else:
                rate = 0

        else:
            rate = None

        vendor.fulfillment_rate = rate

        vendor.save(update_fields=["fulfillment_rate"])

# function that evaluates all the performance metrics of the vendor using the above functions
def evaluate_performance():
    evaluate_avg_rating()
    evaluate_on_time_delivery_rate()
    evaluate_response_time()
    evaluate_fulfillment_rate()

# API view for Vendor
class VendorView(APIView):
    # added authorization
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # function for dealing with GET requests
    def get(self, request, pk=None):
        evaluate_performance()
        if pk:
            try:
                vendor = Vendor.objects.get(id=pk)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Exception:
                return Response({"error": f"vendor with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                vendors = Vendor.objects.all()
                serializer = VendorSerializer(vendors, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    # function for dealing with POST requests
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "there are some errors in the json body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # function for dealing with PUT requests
    def put(self, request, pk=None):
        if pk:
            try:
                vendor = Vendor.objects.get(pk=pk)
                serializer = VendorSerializer(
                    vendor, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "there are some errors in the json body"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"error": f"vendor with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": f"enter a valid id"}, status=status.HTTP_404_NOT_FOUND)
    # function for dealing with DELETE requests
    def delete(self, request, pk=None):
        if pk:
            vendor = Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "enter a valid vendor id"}, status=status.HTTP_400_BAD_REQUEST)

# API view for Purchase Orders
class PurchaseOrderView(APIView):
    # for authorization
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # function for dealing with GET requests
    def get(self, request, pk=None):
        if pk:
            try:
                orders = PurchaseOrder.objects.get(id=pk)
                serializer = POSerializer(orders)
                return Response(serializer.data)
            except Exception:
                return Response({"error": f"order with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                get_data = request.query_params

                if "vendor" not in get_data:
                    orders = PurchaseOrder.objects.all()
                else:
                    try:
                        orders = PurchaseOrder.objects.filter(
                            vendor=get_data["vendor"])
                    except Exception:
                        return Response({"error": "enter a valid vendor id"}, status=status.HTTP_400_BAD_REQUEST)

                serializer = POSerializer(orders, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    # function for dealing with POST requests
    def post(self, request):
        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            evaluate_performance()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "there are some errors in the json body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # function for dealing with PUT requests
    def put(self, request, pk=None):
        if pk:
            try:
                order = PurchaseOrder.objects.get(pk=pk)
                serializer = POSerializer(
                    order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    evaluate_performance()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "there are some errors in the json body"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"error": f"order with id {pk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": f"enter a valid id"}, status=status.HTTP_404_NOT_FOUND)
    # function for dealing with DELETE requests
    def delete(self, request, pk=None):
        if pk:
            order = PurchaseOrder.objects.get(pk=pk)
            order.delete()
            evaluate_performance()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "enter a valid order id"}, status=status.HTTP_400_BAD_REQUEST)

# API view for Historical Performance of Vendors
class HistoricalPerformanceView(APIView):
    # for authorization
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # function for GET requests
    def get(self, request, pk=None):
        if pk:
            try:
                vendor = Vendor.objects.get(id=pk)
                history = HistoricalPerformance.objects.filter(vendor=pk)
                serializer = HPSerializer(history, many=True)
                if serializer.data:
                    return Response(serializer.data)
                else:
                    return Response({"info": "this vendor doesn't have any records"}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "enter a valid vendor id"}, status=status.HTTP_404_NOT_FOUND)
            
# API view for Acknowledging Purchase Orders
class AcknowledgmentView(APIView):
    # for authorization
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # function to deal with the POST request
    def post(self, request, pk=None):
        if pk:
            try:
                order = PurchaseOrder.objects.get(pk=pk)
                if order.acknowledgment_date:
                    return Response({"error": "this order has already been acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = POSerializer(order, data={"acknowledgment_date": datetime.now()}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    evaluate_performance()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({"error": "order id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "enter a valid id"}, status=status.HTTP_400_BAD_REQUEST)

# API view for  getting the Authorization Token
class GetToken(APIView):
    def get(self, request):
        try:
            User = get_user_model()
            u = User.objects.get(username="admin")
            token, created = Token.objects.get_or_create(user=u)

            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

