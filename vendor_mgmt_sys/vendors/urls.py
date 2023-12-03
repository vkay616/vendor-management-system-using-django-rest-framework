from django.urls import path, include
from . import views


urlpatterns = [
    path("vendors/", views.VendorView.as_view(), name="vendor-list"),
    path("vendors/<int:pk>/", views.VendorView.as_view(), name="vendor-by-id")    ,
]