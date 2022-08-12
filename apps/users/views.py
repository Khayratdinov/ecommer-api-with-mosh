from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin,  UpdateModelMixin
# ============================================================================ #
from apps.users.models import Customer
from apps.users.serializers import CustomerSerializer
# Create your views here.


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, GenericViewSet ):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer