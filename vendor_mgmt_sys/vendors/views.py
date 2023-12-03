from django.shortcuts import render
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendorSerializer

class VendorView(APIView):

    def get(self, request, pk=None):
        if pk:
            vendor = Vendor.objects.get(id=pk)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)
        
    